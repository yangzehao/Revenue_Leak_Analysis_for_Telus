# Revenue_Leak_Analysis_for_Telus
This project analyzed the reason of avenue leakage based on the Telus overage and credit return data. It offers some useful suggestions to deal with the revenue leakage for telecommunication companies. The data source is excel. The process involves data extraction, cleaning, transformation and analytics. There are three relational tables in this project. It should be noted that the privacy information, such as phone numbers and account numbers, has been encoded for this open access version. That means they are not related to a real person now :). The purposes of giving the open access to this project are (1) to help others in the telecommnications industry have more insight into revenue leakage data; (2) to share my data manipulation and analytics experience. The report in this repository presents the detail of the discussion and results for this project.

## 1. The Platform:
	The OS is MacOS Catalina 10.15.7
	The CPU is 2.4 GHz 8-Core Intel Core i9
	The GPU is AMD Radeon Pro 5500M 8G

## 2. The programming language and IDE:
Python and PyCharm

## 3. The third-party packages used in this project:
pandas, numpy, matplotlib and openpyxl
The openpyxl is used by pandas as an engine to read the xlsx file (pip install openpyxl if the codes are tested)

## 4. The description of each file:
(1) There are four python modules to deal with this project:
The data_initial_analysis module is used to analyze three relational tables roughly. This is an important step before we begin join or transform the tables.
The keys' relationship, such as many-to-many, should be clarified in this step;

The leakage_analysis.py module is used to calculate the segment leakage, and some information obtained from data_initial_analysis module is used. This module offers the information to answer the question one in the report;

The trend_analysis.py module is used to analyze the trend of overage, max policy credit (=policy(overage)) and real credit return. Several tables are obtained through data cleaning, transformation and wrangling. These tables are used for the data visulization and answering the questions 2-4 in the report;

The policy.py module is the TELUS policy function. It is used to calculate the max policy credit return. If the real credit return in the Credits table is larger than this calculated max policy credit return, the revenue leakage is generaged. Revenue Leakage = Real Credit - Max Policy Credit. Max Policy Credit = policy (overage). The max coefficients in the policy function are applied.

(2) Revenue Leakage Analysis Report for Telus. This is the results and discussion for this project. It includes all the information coming from the four python modules mentioned above. It answers the four questions in this project. 

## 5. Others:
The modules (leakage_analysis, trend_analysis and data_initial analysis) can be executed separately. Each module used the pandas with openpyxl engine to read the xlsx. The reading process takes the most time during the code execution. The speed can be faster if we put all the code in one module and read the file once. However, the readability would be sacrificed.


Thanks.
John
