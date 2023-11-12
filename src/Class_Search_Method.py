import pandas as pd
from pathlib import Path

class Local_Course_Catalogue:
    
    directory_path = ""
    course_data = pd.DataFrame()
    all_search_results = pd.DataFrame()
    current_displayed_search_results = pd.DataFrame()
    
    num_of_search_results_shown = 0
    current_displayed_search_results_start_iterator = 0
    current_displayed_search_results_end_iterator = -1
    
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.course_data = pd.DataFrame()
        self.all_search_results = pd.DataFrame()
        self.current_displayed_search_results = pd.DataFrame()
        
        self.num_of_search_results_shown = 0
        self.current_displayed_search_results_start_iterator = 0
        self.current_displayed_search_results_end_iterator = -1
        
        self.collect_course_data()
        
    def collect_course_data(self):
        csv_files = Path(self.directory_path).glob("*.csv")
        for f in csv_files:
            self.course_data = pd.concat([self.course_data, pd.read_csv(f, dtype = str, index_col = False)])
    
    
    def top_results(self):
        self.current_displayed_search_results = self.all_search_results.iloc[:self.current_displayed_search_results_end_iterator]
        return self.current_displayed_search_results
    
    def show_next_n_results(self):
        self.current_displayed_search_results_start_iterator = self.current_displayed_search_results_start_iterator + self.num_of_search_results_shown
        self.current_displayed_search_results_end_iterator = self.current_displayed_search_results_end_iterator + self.num_of_search_results_shown
        
        self.current_displayed_search_results = self.all_search_results.iloc[self.current_displayed_search_results_start_iterator:self.current_displayed_search_results_end_iterator]
        print(self.current_displayed_search_results)
        return self.current_displayed_search_results
    
    def show_previous_n_results(self):
        self.current_displayed_search_results_start_iterator = self.current_displayed_search_results_start_iterator - self.num_of_search_results_shown
        if (self.current_displayed_search_results_start_iterator < 0):
            self.current_displayed_search_results_start_iterator = 0
        
        self.current_displayed_search_results_end_iterator = self.current_displayed_search_results_start_iterator + self.num_of_search_results_shown
        
        self.current_displayed_search_results = self.all_search_results.iloc[self.current_displayed_search_results_start_iterator:self.current_displayed_search_results_end_iterator]
        print(self.current_displayed_search_results)
        return self.current_displayed_search_results
        
    
    def search_course_catalogue_by_terms(self, num_of_entries_to_display = -1, input_abbreviation = "", input_name = "", input_course_level = "", input_credit_hours = "", input_description_keyphrase = "", input_terms_offered = "", input_grade_mode = ""):
        self.current_displayed_search_results_start_iterator = 0
        self.all_search_results = self.course_data
        if len(input_abbreviation) > 0:
            self.all_search_results = self.all_search_results[self.all_search_results["code"].str[0:len(input_abbreviation)] == input_abbreviation]
        
        if len(input_name) > 0:
            self.all_search_results = self.all_search_results[self.all_search_results["name"].str.contains(input_name, na = False)]
        
        if len(input_course_level) == 1:
            self.all_search_results = self.all_search_results[self.all_search_results["code"].str[-3] == input_course_level]
        
        if len(input_credit_hours) > 0:
            self.all_search_results = self.all_search_results[self.all_search_results["credits"].str[0] == input_credit_hours]
        
        if len(input_description_keyphrase):
            self.all_search_results = self.all_search_results[self.all_search_results["description"].str.contains(input_description_keyphrase, na = False)]
        
        if len(input_terms_offered) > 0:
            self.all_search_results = self.all_search_results[self.all_search_results["termsOffered"].str.contains(input_terms_offered, na = False)]
        
        if len(input_grade_mode) > 0:
            self.all_search_results = self.all_search_results[self.all_search_results["gradeMode"].str.contains(input_grade_mode, na = False)]
        
        self.current_displayed_search_results = self.all_search_results
        self.num_of_search_results_shown = len(self.current_displayed_search_results)
        if (num_of_entries_to_display > -1):
            self.num_of_search_results_shown = num_of_entries_to_display
            self.current_displayed_search_results_end_iterator = num_of_entries_to_display
            self.current_displayed_search_results = self.top_results()
        print(self.current_displayed_search_results)
        # maybe make it into a restful API
        return self.current_displayed_search_results

# Testing can be done beyond this point.
test_catalogue = Local_Course_Catalogue("csuCourseCatalogDB")
print("Showing the top results of an initial search: ")
test_catalogue.search_course_catalogue_by_terms(9, "", "", "1", "", "", "", "")
print("The next amount of results after advancing forward in the dataframe: ")
test_catalogue.show_next_n_results()
print("The previous results after rewinding in the dataframe: ")
test_catalogue.show_previous_n_results()