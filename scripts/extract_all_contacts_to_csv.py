#!/usr/bin/env python3
"""
Script to extract all contacts from specifications.md files and Operator-Key-Contacts.md
and create a comprehensive CSV file with name, position, company, country, email, and phone.
"""
import os
import re
import csv
from pathlib import Path

def extract_contacts_from_markdown(content, country=None, company=None):
    """Extract contact information from markdown content."""
    contacts = []
    
    # Pattern to match contact entries with various formats
    # Matches: - **Name**: Name, **Title**: Title, **Email**: email, etc.
    name_pattern = r'\*\*Name\*\*:\s*([^\n]+)'
    title_pattern = r'\*\*Title\*\*:\s*([^\n]+)'
    email_pattern = r'\*\*Email\*\*:\s*([^\n]+)'
    phone_pattern = r'\*\*Phone\*\*:\s*([^\n]+)'
    alternative_email_pattern = r'\*\*Alternative Email\*\*:\s*([^\n]+)'
    
    # Split content into sections that might contain contacts
    # Look for patterns like "**Name**:", "**Title**:", etc.
    sections = re.split(r'(?=\*\*Name\*\*:|\*\*Title\*\*:|\*\*Email\*\*:|\*\*Phone\*\*)', content)
    
    current_contact = {}
    for section in sections:
        # Extract name
        name_match = re.search(name_pattern, section)
        if name_match:
            if current_contact and 'name' in current_contact:
                # Save previous contact if it has a name
                if current_contact.get('name') and current_contact.get('name') != 'OPEN':
                    contacts.append(current_contact)
            current_contact = {'name': name_match.group(1).strip(), 'country': country, 'company': company}
        
        # Extract title
        title_match = re.search(title_pattern, section)
        if title_match:
            current_contact['position'] = title_match.group(1).strip()
        
        # Extract email
        email_match = re.search(email_pattern, section)
        if email_match:
            email = email_match.group(1).strip()
            # Remove "(predicted)" markers
            email = re.sub(r'\s*\(predicted\)', '', email, flags=re.IGNORECASE)
            current_contact['email'] = email
        
        # Extract alternative email
        alt_email_match = re.search(alternative_email_pattern, section)
        if alt_email_match:
            alt_email = alt_email_match.group(1).strip()
            # If we already have an email, we could store this separately or combine
            # For now, we'll use the primary email
            if 'email' not in current_contact:
                current_contact['email'] = alt_email
        
        # Extract phone
        phone_match = re.search(phone_pattern, section)
        if phone_match:
            current_contact['phone'] = phone_match.group(1).strip()
    
    # Don't forget the last contact
    if current_contact and current_contact.get('name') and current_contact.get('name') != 'OPEN':
        contacts.append(current_contact)
    
    return contacts

def extract_country_from_path(file_path):
    """Extract country name from file path."""
    parts = Path(file_path).parts
    if 'Europe' in parts:
        europe_idx = parts.index('Europe')
        if europe_idx + 1 < len(parts):
            country = parts[europe_idx + 1]
            # Clean up country name (remove hyphens, etc.)
            country = country.replace('-', ' ').title()
            return country
    return None

def extract_company_from_path(file_path):
    """Extract company/operator name from file path."""
    parts = Path(file_path).parts
    # Company is usually the directory name before specifications.md
    if 'specifications.md' in parts[-1]:
        company = parts[-2] if len(parts) > 1 else None
        if company:
            # Clean up company name
            company = company.replace('-', ' ').replace('_', ' ')
            # Handle special cases
            if company == 'Ziggo UPC':
                company = 'VodafoneZiggo'
            elif company == 'Tivusat LaTivu':
                company = 'TivuSat'
            elif company == 'Magenta TV':
                company = 'Magenta TV (Deutsche Telekom)'
            elif company == 'Swisscom TV':
                company = 'Swisscom'
            elif company == 'Free France':
                company = 'Free France (Iliad Group)'
            elif company == 'Orange France':
                company = 'Orange France'
            elif company == 'Canal France':
                company = 'CANAL+ Group'
            elif company == 'France 24':
                company = 'France 24'
            return company
    return None

def process_all_files():
    """Process all specifications.md files and master contacts file."""
    all_contacts = []
    base_dir = Path('Europe')
    
    # Process all specifications.md files
    for spec_file in base_dir.rglob('specifications.md'):
        country = extract_country_from_path(spec_file)
        company = extract_company_from_path(spec_file)
        
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
                contacts = extract_contacts_from_markdown(content, country, company)
                all_contacts.extend(contacts)
        except Exception as e:
            print(f"Error processing {spec_file}: {e}")
    
    # Process the master Operator-Key-Contacts.md file
    master_file = Path('Europe/Operator-Key-Contacts.md')
    if master_file.exists():
        try:
            with open(master_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract country and company from section headers
                sections = re.split(r'\n## |\n### ', content)
                for section in sections:
                    # Try to extract country from section header
                    country_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', section)
                    country = country_match.group(1) if country_match else None
                    
                    # Try to extract company from subsection
                    company_match = re.search(r'^###\s+([^\n]+)', section, re.MULTILINE)
                    if not company_match:
                        company_match = re.search(r'^([A-Z][^\n(]+)', section.split('\n')[0] if section else '')
                    company = company_match.group(1).strip() if company_match else None
                    
                    # Clean up company name
                    if company:
                        company = re.sub(r'\s*\([^)]+\)', '', company)  # Remove parenthetical info
                        company = company.strip()
                    
                    contacts = extract_contacts_from_markdown(section, country, company)
                    all_contacts.extend(contacts)
        except Exception as e:
            print(f"Error processing {master_file}: {e}")
    
    # Remove duplicates based on name and email
    seen = set()
    unique_contacts = []
    for contact in all_contacts:
        key = (contact.get('name', '').lower(), contact.get('email', '').lower())
        if key not in seen and contact.get('name'):
            seen.add(key)
            unique_contacts.append(contact)
    
    return unique_contacts

def write_csv(contacts, output_file):
    """Write contacts to CSV file."""
    fieldnames = ['name', 'position', 'company', 'country', 'email', 'phone']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for contact in sorted(contacts, key=lambda x: (
            x.get('country') or '', 
            x.get('company') or '', 
            x.get('name') or ''
        )):
            # Ensure all fields are present
            row = {field: contact.get(field, '') or '' for field in fieldnames}
            writer.writerow(row)

if __name__ == '__main__':
    print("Extracting contacts from all files...")
    contacts = process_all_files()
    print(f"Found {len(contacts)} unique contacts")
    
    output_file = 'Europe/Industry-Contacts-Master.csv'
    write_csv(contacts, output_file)
    print(f"✅ Contacts written to {output_file}")

