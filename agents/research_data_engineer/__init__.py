#!/usr/bin/env python3
"""
Research Data Engineer Agent
A senior research data engineer that extracts, cleans, validates, and stores facts
with source tracking, external data enrichment, and citation management.
"""
from .agent import ResearchDataEngineer
from .database import ResearchDatabase
from .data_cleaner import DataCleaner
from .web_researcher import WebResearcher

__all__ = [
    'ResearchDataEngineer',
    'ResearchDatabase',
    'DataCleaner',
    'WebResearcher'
]

__version__ = '1.0.0'
