-- ============================================
-- SKILLSCOUT DATABASE SCHEMA
-- ============================================
-- Version: 1.1
-- Author: ZN-0X
-- Date: December 24, 2025
-- Description: PostgreSQL schema for job market analytics
-- ============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- LOOKUP TABLES
-- ============================================

CREATE TABLE industries (
    industry_id UUID DEFAULT uuid_generate_v4(),
    industry_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (industry_id)
);

CREATE TABLE skill_categories (
    category_id UUID DEFAULT uuid_generate_v4(),
    category_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id)
);

CREATE TABLE platforms (
    platform_id UUID DEFAULT uuid_generate_v4(),
    platform_name TEXT NOT NULL UNIQUE,
    base_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (platform_id)
);

CREATE TABLE locations (
    location_id UUID DEFAULT uuid_generate_v4(),
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (location_id),
    UNIQUE (city, country)
);

-- ============================================
-- MAIN TABLES
-- ============================================

CREATE TABLE companies (
    company_id UUID DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    industry_id UUID REFERENCES industries(industry_id) ON DELETE SET NULL,
    size TEXT,
    location_id UUID REFERENCES locations(location_id) ON DELETE SET NULL,
    website TEXT,
    linkedin_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id)
);

CREATE TABLE skills (
    skill_id UUID DEFAULT uuid_generate_v4(),
    skill_name TEXT NOT NULL UNIQUE,
    category_id UUID REFERENCES skill_categories(category_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (skill_id)
);

CREATE TABLE jobs (
    job_id UUID DEFAULT uuid_generate_v4(),
    external_id TEXT,
    title TEXT NOT NULL,
    company_id UUID REFERENCES companies(company_id) ON DELETE CASCADE,
    description TEXT,
    requirements TEXT,
    benefits TEXT,
    employment_type TEXT,
    job_shift TEXT,
    is_remote BOOLEAN DEFAULT false,
    total_positions INTEGER,
    gender VARCHAR(1),
    min_experience TEXT,
    min_salary INTEGER,
    max_salary INTEGER,
    job_level TEXT,
    salary_currency VARCHAR(3) DEFAULT 'PKR',
    application_url TEXT,
    apply_before DATE,
    posted_date TIMESTAMP,
    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id)
);

-- ============================================
-- JUNCTION TABLES
-- ============================================

CREATE TABLE job_skills(
    job_id UUID REFERENCES jobs(job_id),
    skill_id UUID REFERENCES skills(skill_id),
    is_required BOOLEAN DEFAULT true,
    experience_level NUMERIC,
    PRIMARY KEY(job_id, skill_id)
);

CREATE TABLE job_platforms (
    job_id UUID REFERENCES jobs(job_id),
    platform_id UUID REFERENCES platforms(platform_id),
    source_url TEXT,
    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id,platform_id)
);

CREATE TABLE job_locations (
    job_id UUID REFERENCES jobs(job_id),
    location_id UUID REFERENCES locations(location_id),
    PRIMARY KEY (job_id, location_id)
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_jobs_company_id ON jobs(company_id);
CREATE INDEX idx_jobs_is_active ON jobs(is_active);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX idx_jobs_apply_before ON jobs(apply_before);
CREATE INDEX idx_jobs_salary ON jobs(min_salary, max_salary);
CREATE INDEX idx_companies_industry_id ON companies(industry_id);
CREATE INDEX idx_companies_location_id ON companies(location_id);
CREATE INDEX idx_skills_category_id ON skills(category_id);
CREATE INDEX idx_job_skills_skill_id ON job_skills(skill_id);
CREATE INDEX idx_job_skills_job_id ON job_skills(job_id);
CREATE INDEX idx_job_platforms_platform_id ON job_platforms(platform_id);
CREATE INDEX idx_job_locations_location_id ON job_locations(location_id);