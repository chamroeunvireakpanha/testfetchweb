import csv
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

class SchoolAssessmentAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def process_file(self, file_path):
        """Opens and reads the content of the file (CSV, Excel, or TXT)."""
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    # Custom logic for plain text files (assuming tab-separated)
                    self.data = pd.read_csv(file_path, delimiter='\t')
            print(f"Data loaded successfully from {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    def transfer_data(self, criteria, source_file, destination_file):
        """Transfers data based on predefined criteria and saves to a new file."""
        try:
            # Load the source file
            self.process_file(source_file)

            # Filter based on criteria
            filtered_data = self.data.query(criteria)
            filtered_data.to_csv(destination_file, index=False)
            print(f"Data successfully transferred to {destination_file}")
        except Exception as e:
            print(f"Error transferring data: {e}")

    def fetch_web_data(self, url):
        """Fetches data from a school webpage using urlopen and parses the HTML content."""
        try:
            with urlopen(url) as response:
                soup = BeautifulSoup(response, 'html.parser')
                # Example logic to extract relevant data from the webpage
                data = soup.find_all('div', class_='assessment-details')
                extracted_data = [item.get_text() for item in data]
                # Process or store the extracted data as needed
                print(f"Web data extracted from {url}: {extracted_data}")
                return extracted_data
        except Exception as e:
            print(f"Error fetching web data from {url}: {e}")
            return None

    def analyze_content(self):
        """Analyzes the assessment data, identifying trends, averages, and performance metrics."""
        try:
            if not self.data.empty:
                average_score = self.data['Score'].mean()
                top_class = self.data.groupby('Class')['Score'].mean().idxmax()
                print(f"Average Score: {average_score:.2f}, Top Class: {top_class}")
                return {"average_score": average_score, "top_class": top_class}
            else:
                print("No data available for analysis.")
                return None
        except Exception as e:
            print(f"Error analyzing content: {e}")

    def generate_summary(self):
        """Generates a summary report for the school principal with key insights."""
        try:
            analysis_results = self.analyze_content()
            if analysis_results:
                summary = f"""
                School Assessment Summary Report:

                1. Overall Performance:
                   - Average score: {analysis_results['average_score']:.2f}
                   - Top-performing class: {analysis_results['top_class']}

                Report generated on: 2024-01-14
                """
                return summary
            else:
                return "No summary available."
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

# Example Usage
analyzer = SchoolAssessmentAnalyzer()

# Process files
analyzer.process_file('school_management.csv')
analyzer.process_file('school_management.xlsx')

# Transfer data
analyzer.transfer_data('score > 90', 'school_management.csv', 'high_achievers.csv')

# Fetch web data
analyzer.fetch_web_data('http://localhost:8000/test_assessment_page.html')

# Analyze content
analyzer.analyze_content()

# Generate summary
summary = analyzer.generate_summary()
print(summary)
