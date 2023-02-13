# other_projects

A recopilation of smaller Data Science works I've been involved in.

## German credit analysis

This is a very popular and well-known dataset that can be found in the UCI repository [1]. The dataset used to deal with this problem was provided by my teaching staff at the Universitat Oberta de Catalunya as part of my data mining course, and it includes the target variable which is not included in the UCI version. The dataset can be difficult to understand if it is seen without context, however, the UCI website includes some explanations about the variables.

To get better results, a selection of the variables has been performed.

|  Algorithm | Accuracy (%) |
| ---------- | ------------ |
| Decision Tree | 71.26 |
| Random Forest | 70.06 |
| Naive Bayes | 71.26 |
| Logistic Regression | 71.26 |

The goal of the analysis has been to compare different algorithms that don't need any alteration of the dataset's original non-numeric discrete nature of the variables.  It has been interesting to see how all of these give fairly similar accuracies of around 70%, which leaves room for improvement. Furthermore, the current approach seems to make the accuracy cap at 71.26. Therefore, in a future iteration of the analysis, some rethinking of it should be done, such as a transformation of the variables to numeric and scaling, or the addition of an unsupervised approach. Also, outliers might have had an impact in the final result, so these should be observed as well.    

## Supermarket prices scraper

This project includes two Python files that scrape a Spanish supermarket's website to obtain a .csv file with every product's price in it. It was completed in association with one of my master's fellow students, [Mikel Álvarez Rua](https://www.linkedin.com/in/mikel-alvarez-rua/), and originaly yielded a file with 7096 product names and prices, providing endless possibilities for Machine Learning.

In order to comply with the Spanish data legislation, no details of the supermarket will be provided, and every URL in the original project is replaced with a fictional one. A sample of the obtained .csv file is shown in the following table with fictional product names to provide a sense of the result.

| Section | Product | Price (€)|
| ---------- | ------------ | -------- |
| Prepared meals | Spanish Omelette 250 gr | 1.5 |
| Prepared meals | Spaguetti with Meatballs 250 gr | 3.49 |
| Prepared meals | Spanish Paella 280 gr | 1.9 |
| Fresh produce | Cherry tomatoes 250 gr | 0.99 |
| Fresh produce | Organic carrots 400 gr | 1.35 |
| Meat and cheese | Sausages with cheddar cheese 3 x 150 gr | 3.15 |

## Time series analysis

This work analyzes a time series that shows airline users with a monthly granularity [2]. It is decomposed in the typical components of a time series to better understand the data's structure.

Once the data is decomposed, a prediction of the last two years of the data can be made, along with a possible spectrum of that prediction in terms of max and min values.



## Bibliography

[1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

