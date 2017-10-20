# data607-project3


### Scraping Setup - John Grando

#### Technical

- Indeed.com was used for this project.
- 100 mile radii for the 10 largest cities, by population, were selected for the job posting areas.
- Common words found by observation were dropped using the drop_l list.
- For each location, the job postings from the first page (50) were scraped and all data within the `<p>` and `<li>` tags were returned.
- If the link selected had already been scraped (based on the first 100 characters of the url) then the link was passed over.
- For each object returned, a single list was compiled for the entire job posting and then tokenized.
- Common "stop words" were then removed along with the drop_l words.
- Frequency distributions were then performed on the resulting list, the resulting list in bigrams form, and the resulting list in trigrams form.
- The location, job title, link, processed list, and frequency distribution results (50 most common for single, bigram, trigram) were then saved in the following files:
  - Per job posting - links_data_LOCATION_.csv
  - Per location - links_summary_data.csv
  - Per entire study - links_global_summary_data.csv
- Additionally, the "Desired Experience" section from each job posting was scraped and saved in the following files:
  - Per location - links_exp_summary_data.csv
  - Per entire study - links_exp_global_summary_data.csv

#### Presentation
- Data was collected from Indeed.com
  - Actual job posting
  - Desired Experience section
- Study was set up to return job postings from the 10 largest cities by population
- Efforts were taken to automatically exclude duplicate postings
- Data was then tokenized and common words (traditional stop words and custom selection of words) were removed.
- Simple frequency distributions for single, bigram, and trigrams, were then performed and resulting data was saved to csv files on github.
- Data exists on the following levels:
  - Individual Posting
  - By location
  - Full study
