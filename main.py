#!/usr/bin/env python3
"""
Daily Stock Analysis - Main Entry Point

This module serves as the primary entry point for the daily stock analysis tool.
It orchestrates data fetching, analysis, and report generation.
"""

import os
import sys
import logging
import argparse
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/analysis_{date.today().strftime('%Y%m%d')}.log"),
    ],
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments for the stock analysis tool."""
    parser = argparse.ArgumentParser(
        description="Daily Stock Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbols AAPL MSFT GOOGL
  python main.py --symbols TSLA --date 2024-01-15
  python main.py --config config.yaml --output reports/
        """,
    )

    parser.add_argument(
        "--symbols",
        nargs="+",
        help="Stock ticker symbols to analyze (e.g., AAPL MSFT)",
        default=None,
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().strftime("%Y-%m-%d"),
        help="Analysis date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.getenv("OUTPUT_DIR", "reports"),
        help="Output directory for generated reports",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose/debug logging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run analysis without saving output files",
    )

    return parser.parse_args()


def setup_directories(output_dir: str) -> None:
    """Create necessary directories if they don't exist."""
    dirs = [output_dir, "logs", "data/cache"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def main():
    """Main execution function for daily stock analysis."""
    args = parse_arguments()

    # Update logging level if verbose mode
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    # Setup required directories
    setup_directories(args.output)

    logger.info(f"Starting Daily Stock Analysis for date: {args.date}")
    logger.info(f"Output directory: {args.output}")

    # Resolve symbols from args or environment variable
    symbols = args.symbols
    if not symbols:
        env_symbols = os.getenv("STOCK_SYMBOLS", "")
        symbols = [s.strip() for s in env_symbols.split(",") if s.strip()]

    if not symbols:
        logger.error("No stock symbols provided. Use --symbols or set STOCK_SYMBOLS in .env")
        sys.exit(1)

    logger.info(f"Analyzing {len(symbols)} symbol(s): {', '.join(symbols)}")

    try:
        analysis_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        logger.error(f"Invalid date format: {args.date}. Expected YYYY-MM-DD")
        sys.exit(1)

    # Placeholder for pipeline execution — modules will be wired in subsequent commits
    logger.info("Analysis pipeline initialized. Ready for module integration.")
    logger.info(f"Dry run mode: {args.dry_run}")

    logger.info("Daily stock analysis completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
