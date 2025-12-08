"""
PHARMA AI - Configuration Module
Centralized configuration management for Pharma Innovation AI System
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import logging


class Settings(BaseSettings):
    """
    Application settings using Pydantic v2 BaseSettings
    Loads configuration from .env file and environment variables
    """

    # ═══════════════════════════════════════════════════════════════════════════════
    # API Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    api_title: str = "Pharma Innovation AI"
    api_description: str = "Agentic AI system for pharmaceutical innovation opportunity discovery"
    api_version: str = "1.0.0"


    # ═══════════════════════════════════════════════════════════════════════════════
    # OpenAI / LLM Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4")
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    llm_timeout: int = 30  # seconds


    # ═══════════════════════════════════════════════════════════════════════════════
    # Database Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./pharma_ai.db")
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10


    # ═══════════════════════════════════════════════════════════════════════════════
    # Redis Cache Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    enable_caching: bool = True
    cache_ttl_hours: int = 24
    cache_ttl_seconds: int = 86400  # 24 hours


    # ═══════════════════════════════════════════════════════════════════════════════
    # Monitoring & Logging Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    enable_monitoring: bool = True
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN", None)
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


    # ═══════════════════════════════════════════════════════════════════════════════
    # Third-party APIs Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    pubmed_api_key: Optional[str] = os.getenv("PUBMED_API_KEY", None)
    pubmed_base_url: str = "https://pubmed.ncbi.nlm.nih.gov"
    
    iqvia_api_key: Optional[str] = os.getenv("IQVIA_API_KEY", None)
    iqvia_base_url: str = "https://api.iqvia.com"
    
    exim_api_key: Optional[str] = os.getenv("EXIM_API_KEY", None)
    exim_base_url: str = "https://api.exim.com"


    # ═══════════════════════════════════════════════════════════════════════════════
    # Report Generation Settings
    # ═══════════════════════════════════════════════════════════════════════════════
    
    enable_pdf_generation: bool = True
    pdf_page_size: str = "letter"
    pdf_font_name: str = "Helvetica"
    pdf_font_size: int = 10


    # ═══════════════════════════════════════════════════════════════════════════════
    # Pydantic v2 Configuration
    # ═══════════════════════════════════════════════════════════════════════════════
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env
    )


    # ═══════════════════════════════════════════════════════════════════════════════
    # Path Properties (computed after initialization)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    @property
    def project_root(self) -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent


    @property
    def output_dir(self) -> Path:
        """Get output directory for all generated files"""
        return self.project_root / "outputs"


    @property
    def reports_dir(self) -> Path:
        """Get reports directory for PDF outputs"""
        return self.output_dir / "reports"


    @property
    def data_dir(self) -> Path:
        """Get data directory for processed data files"""
        return self.output_dir / "data"


    @property
    def logs_dir(self) -> Path:
        """Get logs directory for application logs"""
        return self.output_dir / "logs"


    @property
    def cache_dir(self) -> Path:
        """Get cache directory for temporary cache files"""
        return self.output_dir / "cache"


    @property
    def temp_dir(self) -> Path:
        """Get temporary directory for temporary files"""
        return self.project_root / "tmp"


    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def __init__(self, **data):
        """Initialize settings and create required directories"""
        super().__init__(**data)
        
        # Create all required directories
        self._create_directories()
        
        # Validate settings
        self._validate_settings()
        
        # Setup logging
        self._setup_logging()


    def _create_directories(self) -> None:
        """Create all required directories"""
        directories = [
            self.output_dir,
            self.reports_dir,
            self.data_dir,
            self.logs_dir,
            self.cache_dir,
            self.temp_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


    def _validate_settings(self) -> None:
        """Validate critical settings"""
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not set. "
                "Please set OPENAI_API_KEY environment variable or in .env file"
            )
        
        if not self.llm_model:
            raise ValueError("LLM_MODEL not configured")


    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=self.log_level,
            format=self.log_format,
            handlers=[
                logging.FileHandler(self.logs_dir / "pharma_ai.log"),
                logging.StreamHandler()
            ]
        )


    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def get_cache_key(self, prefix: str, identifier: str) -> str:
        """Generate a cache key"""
        return f"{prefix}:{identifier}"


    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.debug


    def get_log_file(self) -> Path:
        """Get main log file path"""
        return self.logs_dir / "pharma_ai.log"


    def get_report_path(self, filename: str) -> Path:
        """Get full path for a report file"""
        return self.reports_dir / filename


    def dict(self, **kwargs):
        """Return settings as dictionary (excluding sensitive data)"""
        data = super().model_dump(**kwargs)
        # Remove sensitive keys
        sensitive_keys = ['openai_api_key', 'pubmed_api_key', 'iqvia_api_key', 'exim_api_key', 'sentry_dsn', 'redis_url']
        for key in sensitive_keys:
            if key in data:
                data[key] = "***REDACTED***"
        return data


    def __repr__(self) -> str:
        """String representation of settings"""
        return f"<Settings: {self.api_title} v{self.api_version}>"


# ═══════════════════════════════════════════════════════════════════════════════
# Initialize Global Settings Instance
# ═══════════════════════════════════════════════════════════════════════════════

try:
    settings = Settings()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    raise
