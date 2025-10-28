#!/usr/bin/env python3
import argparse
import os
import sys
from utils.io_utils import read_input_file, write_output_file
from utils.search_providers import LinkedInSearcher
from utils.linkedin_utils import validate_linkedin_url, fetch_profile_latest_job


def parse_args():
    parser = argparse.ArgumentParser(
        description="Enrich input CSV/XLSX by finding and validating LinkedIn URLs and latest job info"
    )
    parser.add_argument(
        "input_path",
        help="Path to input file (.csv or .xlsx) with columns: account_name, contact_persona, designation, Linkedin url",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        default=None,
        help="Path to write enriched output (.csv or .xlsx). Defaults to <input>_enriched.csv",
    )
    parser.add_argument(
        "--engine",
        choices=["duckduckgo", "serpapi"],
        default="duckduckgo",
        help="Search engine to use. serpapi requires SERPAPI_KEY env var.",
    )
    parser.add_argument(
        "--user-agent",
        default=None,
        help="Optional custom User-Agent for validation/profile fetch",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout seconds for validation/profile fetch",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Max search results to consider for each query",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    df = read_input_file(args.input_path)

    searcher = LinkedInSearcher(engine=args.engine, max_results=args.max_results)

    # Ensure expected columns exist; allow flexible casing/spacing
    required_cols = ["account_name", "contact_persona", "designation", "Linkedin url"]
    normalized = {c.lower().strip(): c for c in df.columns}
    for col in required_cols:
        key = col.lower().strip()
        if key not in normalized:
            sys.exit(f"Missing required column: {col}")

    # Prepare output columns
    if "validated_linkedin_url" not in df.columns:
        df["validated_linkedin_url"] = ""
    if "New company" not in df.columns:
        df["New company"] = ""
    if "New job title" not in df.columns:
        df["New job title"] = ""

    for idx, row in df.iterrows():
        account_name = row[normalized["account_name"]]
        persona = row[normalized["contact_persona"]]
        designation = row[normalized["designation"]]
        existing_url = row.get(normalized.get("linkedin url", "Linkedin url"), "")

        # Prefer validating existing URL if present; else search. If invalid, fall back to search.
        candidate_urls = []
        if isinstance(existing_url, str) and existing_url.strip():
            candidate_urls.append(existing_url.strip())
        # Always prepare a search list as fallback
        query = f"{account_name} {persona} {designation} site:linkedin.com/in"
        search_urls = searcher.search(query)

        validated_url = None
        for url in candidate_urls + search_urls:
            if validate_linkedin_url(url, user_agent=args.user_agent, timeout=args.timeout):
                validated_url = url
                break

        df.at[idx, "validated_linkedin_url"] = validated_url or ""

        if validated_url:
            latest_company, latest_title = fetch_profile_latest_job(
                validated_url, user_agent=args.user_agent, timeout=args.timeout
            )
            # If company or title differ from input, set New company/title; else blank
            new_company = ""
            new_title = ""
            if latest_company and isinstance(account_name, str) and account_name:
                if latest_company.strip().lower() != str(account_name).strip().lower():
                    new_company = latest_company
            elif latest_company:
                new_company = latest_company

            if latest_title and isinstance(designation, str) and designation:
                if latest_title.strip().lower() != str(designation).strip().lower():
                    new_title = latest_title
            elif latest_title:
                new_title = latest_title

            df.at[idx, "New company"] = new_company
            df.at[idx, "New job title"] = new_title
        else:
            df.at[idx, "New company"] = ""
            df.at[idx, "New job title"] = ""

    output_path = args.output_path
    if not output_path:
        base, ext = os.path.splitext(args.input_path)
        output_path = f"{base}_enriched.csv"

    write_output_file(df, output_path)
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
