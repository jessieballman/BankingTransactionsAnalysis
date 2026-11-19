# Project Overview
    This was an End-to-End Data Analyst Project that examined:
        * Transaction trends over the entire time period.
        * The breakdown of categories, channels, and transaction types.
        * Customer activity.
        * Distribution of account types.
        * Differences in transactions by country and city within those countries.
        * Differences in the behavior of customers with different risk profiles.
        * Suspicious transactions.
## Dataset
    Dataset used: 
    https://sqlshed.com/practice-datasets/banking-transactions/

    Due to the structural characteristics of the selected dataset, some areas of analysis were adjusted or narrowed. A number of calculated indicators exhibit variability that slightly exceeds the standard permissible error. Nevertheless, there is sufficient data to identify key behavioral patterns and test analytical hypotheses.
## Original Task

    ### The task was set by ChatGPT

    Conduct a comprehensive analysis of banking transactions to investigate customer activity, banking product usage, service channel preferences, and potential anomalies in transaction behavior.

    The analysis should cover the following areas:

    ### Time-Based Analysis

        *Examine changes in transaction volumes and total transaction amounts over time.
        *Identify temporal trends and potential seasonal patterns.

    ### Transaction Analysis

        *Identify the most common transaction types.
        *Examine transaction distributions across banking channels and merchant categories.
        *Analyze the distribution of accounts across different categories.

    ### Customer Analysis

        *Investigate customer activity.
        *Identify the most active customers.

    ### Geographical Analysis

        *Compare transaction activity across countries and cities.
        *Investigate geographical differences in banking service usage.
        *Examine potential discrepancies between the number of customers and transaction volumes across geographical regions.

    ### Risk Analysis

        *Investigate differences in transaction behavior among customers with different risk classifications.
        *Compare transaction characteristics, service channels, activity levels, and other available metrics.
        *Identify potentially unusual patterns without automatically classifying them as fraudulent activity.

    ### Expected Deliverables

        Prepare an analytical report containing visualizations, comparative tables, and findings that provide an overview of banking transaction behavior and highlight potentially meaningful patterns within the dataset.

## Tools
    * **Language:** Python 3.12
    * **Data Processing & Analysis:** Pandas, NumPy
    * **Visualization:** Matplotlib, Seaborn, fontTools
    * **Database & Queries:** PostgreSQL, SQL, sqlalchemy
    * **Environment:** VS Code

## Project Outcomes
    ### Time-Based Analysis
        The number and total value of transactions remain stable throughout the entire observation period, with the exception of seasonal spikes from October through January, when both the number and total value of transactions rise sharply.
    ### Transaction Analysis
        By far the most common type of transaction is card payment (46.24% of all transactions), followed by direct debit (11.92% of all transactions) and transfers in and out (7.96% and 9.03% of all payments, respectively).

        The most common transaction channel is still the card (43.98% of all transactions), followed by online (28.85% of all transactions) and mobile (17.07% of all transactions). Demand for ATMs and bank branches is fairly low (4.04% and 6.06%, respectively).

    ### Customer Analysis
        An analysis of the relationship between the number of transactions and the registration date revealed almost no correlation. An analysis of the relationship between the number of transactions and the average receipt amount showed that customers with an average receipt amount of ~$250 were the most active. A comparison of the number of transactions among users by risk band showed that, on average, their activity levels were nearly identical; however, the most active users fell into the “undefined” risk band.Strangely, a negative correlation was found between a customer's ID and the number of transactions they made, even though the customer's ID does not depend on anything.

        The most active customers were:
            #1 Andres Bauer, client_id=1, number of transactions = 54,637
            #2 Raj Quinn, client_id=2, number of transactions = 21,604
            #3 Claire Frost, client_id=3, number of transactions = 14,829

    ### Geographical Analysis
        The average and median transaction amounts in all countries differ by a margin of error. The median number of transactions is also roughly the same across all countries. Spain stands out significantly in terms of the average number of transactions due to a single customer with the highest number of transactions in the entire bank and a small customer base.

        The difference in the channels used across all countries is within the margin of error.

        The distribution of various risk ranges within countries does not show any significant differences; however, in some countries, certain risk ranges do stand out compared to those in other countries.

        The United States is the most popular country among all of the bank's customers and also leads in the number of bank branches. In terms of the number of transactions, it is surpassed only by Spain, due to a single customer with over 54,000 transactions—a figure that nearly matches the total number of transactions in the United States.

    ### Risk Analysis
        The heat map based on z-score analysis shows small absolute differences despite thermal variations in most columns; however, high-risk and unidentified-risk customers, on average, have significantly more bank accounts (9.25 for high risk and 5.74 for unidentified risk, compared to 2.9 for medium risk and 3.26 for low risk). Also, the average time between transactions for high-risk and unidentified-risk customers is significantly shorter than for medium- and low-risk customers (83.36 hours for high-risk and 115.87 hours for unidentified-risk, compared to 258.85 hours for medium-risk and 215.79 hours for low-risk). The average number of transactions for high-risk and unidentified-risk clients is higher than for medium- and low-risk clients (2.93 for high-risk and 2.47 for unidentified-risk, compared to 1.19 for medium-risk and 1.51 for low-risk). It can be observed that the unidentified risk category mimics the high-risk category, which may indicate that a certain number of high-risk customers have not yet been classified.

        Suspicious transactions will be moved to a separate table containing the transaction ID and a list of anomalies detected in the transaction.







