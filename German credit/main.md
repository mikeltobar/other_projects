german_credit
================

## Intro & goals

In this study, the focus will be on generating and comprehending a
decision tree using a dataset that provides information on credit
admissions in Germany.

The main goal of the analysis is to predict which combination of values
most frequently lead to a default in the credit payment, getting a set
of rules explaining those combinations.

Another goal of the work will be to compare the performance of four
different algorithms: a decision tree, a random forest, a Naive-Bayes
classifier, and a logistic regression.

We will work with algorithms that can handle non-numeric discrete
observations, and test their limits. The possibilities of this type of
algorithms for this kind of problem will be tested. We will compare each
one’s accuracy regarding this dataset.

## 1. Initial data analysis

``` r
library("e1071")
library("ggplot2")
library("miscset")
library("Boruta")
library("dplyr")
library("e1071")
library("caret")
library("randomForest")
library("rpart")
```

Let’s take a brief look at a sample of the data.

``` r
credit <-read.csv("credit_kaggle.csv", TRUE, ",", fileEncoding = "UTF-8")
head(credit,10)
```

    ##    checking_balance months_loan_duration credit_history    purpose amount
    ## 1            < 0 DM                    6       critical   radio/tv   1169
    ## 2        1 - 200 DM                   48         repaid   radio/tv   5951
    ## 3           unknown                   12       critical  education   2096
    ## 4            < 0 DM                   42         repaid  furniture   7882
    ## 5            < 0 DM                   24        delayed  car (new)   4870
    ## 6           unknown                   36         repaid  education   9055
    ## 7           unknown                   24         repaid  furniture   2835
    ## 8        1 - 200 DM                   36         repaid car (used)   6948
    ## 9           unknown                   12         repaid   radio/tv   3059
    ## 10       1 - 200 DM                   30       critical  car (new)   5234
    ##    savings_balance employment_length installment_rate personal_status
    ## 1          unknown           > 7 yrs                4     single male
    ## 2         < 100 DM         1 - 4 yrs                2          female
    ## 3         < 100 DM         4 - 7 yrs                2     single male
    ## 4         < 100 DM         4 - 7 yrs                2     single male
    ## 5         < 100 DM         1 - 4 yrs                3     single male
    ## 6          unknown         1 - 4 yrs                2     single male
    ## 7    501 - 1000 DM           > 7 yrs                3     single male
    ## 8         < 100 DM         1 - 4 yrs                2     single male
    ## 9        > 1000 DM         4 - 7 yrs                2   divorced male
    ## 10        < 100 DM        unemployed                4    married male
    ##    other_debtors residence_history                 property age
    ## 1           none                 4              real estate  67
    ## 2           none                 2              real estate  22
    ## 3           none                 3              real estate  49
    ## 4      guarantor                 4 building society savings  45
    ## 5           none                 4             unknown/none  53
    ## 6           none                 4             unknown/none  35
    ## 7           none                 4 building society savings  53
    ## 8           none                 2                    other  35
    ## 9           none                 4              real estate  61
    ## 10          none                 2                    other  28
    ##    installment_plan  housing existing_credits default dependents telephone
    ## 1              none      own                2       1          1       yes
    ## 2              none      own                1       2          1      none
    ## 3              none      own                1       1          2      none
    ## 4              none for free                1       1          2      none
    ## 5              none for free                2       2          2      none
    ## 6              none for free                1       1          2       yes
    ## 7              none      own                1       1          1      none
    ## 8              none     rent                1       1          1       yes
    ## 9              none      own                1       1          1      none
    ## 10             none      own                2       2          1      none
    ##    foreign_worker                     job
    ## 1             yes        skilled employee
    ## 2             yes        skilled employee
    ## 3             yes      unskilled resident
    ## 4             yes        skilled employee
    ## 5             yes        skilled employee
    ## 6             yes      unskilled resident
    ## 7             yes        skilled employee
    ## 8             yes mangement self-employed
    ## 9             yes      unskilled resident
    ## 10            yes mangement self-employed

We try to look at the column composition looking for empty values and
the numeric information of each column.

``` r
summary(credit)
```

    ##  checking_balance   months_loan_duration credit_history       purpose         
    ##  Length:1000        Min.   : 4.0         Length:1000        Length:1000       
    ##  Class :character   1st Qu.:12.0         Class :character   Class :character  
    ##  Mode  :character   Median :18.0         Mode  :character   Mode  :character  
    ##                     Mean   :20.9                                              
    ##                     3rd Qu.:24.0                                              
    ##                     Max.   :72.0                                              
    ##      amount      savings_balance    employment_length  installment_rate
    ##  Min.   :  250   Length:1000        Length:1000        Min.   :1.000   
    ##  1st Qu.: 1366   Class :character   Class :character   1st Qu.:2.000   
    ##  Median : 2320   Mode  :character   Mode  :character   Median :3.000   
    ##  Mean   : 3271                                         Mean   :2.973   
    ##  3rd Qu.: 3972                                         3rd Qu.:4.000   
    ##  Max.   :18424                                         Max.   :4.000   
    ##  personal_status    other_debtors      residence_history   property        
    ##  Length:1000        Length:1000        Min.   :1.000     Length:1000       
    ##  Class :character   Class :character   1st Qu.:2.000     Class :character  
    ##  Mode  :character   Mode  :character   Median :3.000     Mode  :character  
    ##                                        Mean   :2.845                       
    ##                                        3rd Qu.:4.000                       
    ##                                        Max.   :4.000                       
    ##       age        installment_plan     housing          existing_credits
    ##  Min.   :19.00   Length:1000        Length:1000        Min.   :1.000   
    ##  1st Qu.:27.00   Class :character   Class :character   1st Qu.:1.000   
    ##  Median :33.00   Mode  :character   Mode  :character   Median :1.000   
    ##  Mean   :35.55                                         Mean   :1.407   
    ##  3rd Qu.:42.00                                         3rd Qu.:2.000   
    ##  Max.   :75.00                                         Max.   :4.000   
    ##     default      dependents     telephone         foreign_worker    
    ##  Min.   :1.0   Min.   :1.000   Length:1000        Length:1000       
    ##  1st Qu.:1.0   1st Qu.:1.000   Class :character   Class :character  
    ##  Median :1.0   Median :1.000   Mode  :character   Mode  :character  
    ##  Mean   :1.3   Mean   :1.155                                        
    ##  3rd Qu.:2.0   3rd Qu.:1.000                                        
    ##  Max.   :2.0   Max.   :2.000                                        
    ##      job           
    ##  Length:1000       
    ##  Class :character  
    ##  Mode  :character  
    ##                    
    ##                    
    ## 

``` r
str(credit)
```

    ## 'data.frame':    1000 obs. of  21 variables:
    ##  $ checking_balance    : chr  "< 0 DM" "1 - 200 DM" "unknown" "< 0 DM" ...
    ##  $ months_loan_duration: int  6 48 12 42 24 36 24 36 12 30 ...
    ##  $ credit_history      : chr  "critical" "repaid" "critical" "repaid" ...
    ##  $ purpose             : chr  "radio/tv" "radio/tv" "education" "furniture" ...
    ##  $ amount              : int  1169 5951 2096 7882 4870 9055 2835 6948 3059 5234 ...
    ##  $ savings_balance     : chr  "unknown" "< 100 DM" "< 100 DM" "< 100 DM" ...
    ##  $ employment_length   : chr  "> 7 yrs" "1 - 4 yrs" "4 - 7 yrs" "4 - 7 yrs" ...
    ##  $ installment_rate    : int  4 2 2 2 3 2 3 2 2 4 ...
    ##  $ personal_status     : chr  "single male" "female" "single male" "single male" ...
    ##  $ other_debtors       : chr  "none" "none" "none" "guarantor" ...
    ##  $ residence_history   : int  4 2 3 4 4 4 4 2 4 2 ...
    ##  $ property            : chr  "real estate" "real estate" "real estate" "building society savings" ...
    ##  $ age                 : int  67 22 49 45 53 35 53 35 61 28 ...
    ##  $ installment_plan    : chr  "none" "none" "none" "none" ...
    ##  $ housing             : chr  "own" "own" "own" "for free" ...
    ##  $ existing_credits    : int  2 1 1 1 2 1 1 1 1 2 ...
    ##  $ default             : int  1 2 1 1 2 1 1 1 1 2 ...
    ##  $ dependents          : int  1 1 2 2 2 2 1 1 1 1 ...
    ##  $ telephone           : chr  "yes" "none" "none" "none" ...
    ##  $ foreign_worker      : chr  "yes" "yes" "yes" "yes" ...
    ##  $ job                 : chr  "skilled employee" "skilled employee" "unskilled resident" "skilled employee" ...

We will inspect the column structure to identify any missing values and
obtain a summary of the numeric information for each column.

The dataset provides a set of personal information for each client,
including their age, occupation, number of years worked, civil status,
etc. The variable ‘default’ indicates whether the credit was paid off or
not. This indicator will be used as the objective variable.

Some variables will require binarization, which will be represented
using “1”s and “0”s.

``` r
credit$default<-gsub(1,0,credit$default)
credit$default<-gsub(2,1,credit$default)
credit$dependents<-gsub(1,0,credit$dependents)
credit$dependents<-gsub(2,1,credit$dependents)
```

## 2. Descriptive analysis

It might interesting to do a visual analysis to see how is the data for
each variable.

``` r
ggplotGrid(ncol = 4,
  lapply(c("checking_balance", "credit_history", "purpose", "savings_balance", "employment_length", "personal_status", "other_debtors", "property", "installment_plan", "housing", "telephone", "foreign_worker", "job", "installment_rate","existing_credits", "residence_history"),
    function(col) {
        ggplot(credit, aes_string(col)) + geom_bar() + coord_flip()
    }))
```

    ## Warning: `aes_string()` was deprecated in ggplot2 3.0.0.
    ## i Please use tidy evaluation ideoms with `aes()`

![](main_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

-   The main “default” classifier shows failure in paying off credit ,
    with “1” indicating missing payments, “0” meaning everything has
    been payed in time.

-   “installment.rate” reflects client payment reliability, with “4”
    being low reliability and “1” meaning consistent payments.

-   “dependents” indicates whether the individual has family to support,
    with “1” meaning they have dependents and “0” meaning no dependents.

-   “foreign_worker”, “other_debtors”, and “installment_plan” are not
    considered relevant to the analysis as most data falls into one
    category.

The following quantitative variables will be studied:
“months_loan_duration”, “amount”, and “age”.

``` r
hist(credit$months_loan_duration,xlab="Credit length (months)", ylab="Clients", main="Clients according to credit duration (in months)")
```

![](main_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

``` r
hist(credit$amount,xlab="Importe", ylab="Clients", main="Clients according to credit amount")
```

![](main_files/figure-gfm/unnamed-chunk-6-2.png)<!-- -->

``` r
hist(credit$age,xlab="Age", ylab="Clients", main="Clients by age")
```

![](main_files/figure-gfm/unnamed-chunk-6-3.png)<!-- -->

Data analysis shows that credit lengths primarily fall between 20-40
months, the majority of credits are considered low-quantity, and the
average client age is around 25-30 years.

To study possible outliers, boxplots of each variable are created.

``` r
boxplot(credit$months_loan_duration, main="Credit duration (months)")
```

![](main_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
boxplot(credit$amount, main="Amount of the credit given")
```

![](main_files/figure-gfm/unnamed-chunk-7-2.png)<!-- -->

``` r
boxplot(credit$age, main="Clients' age")
```

![](main_files/figure-gfm/unnamed-chunk-7-3.png)<!-- -->

Outliers are observed in the upper part of the three boxplots, but are
deemed acceptable values and will not be removed from the sample.

## 3. Logistical regression (for variable selection) and Boruta

To simplify the machine learning process, it is necessary to perform
feature filtering. A logistic regression will be run to get an initial
understanding of the importance of each variable in explaining default.
The most significant variables, typically with a p-value of less than or
equal to 0.05, will be selected. However, the threshold may be relaxed
to 0.1 to include other borderline predictors. The initial selection
will then be refined using the Boruta method, a variable selection
algorithm.

``` r
# Casting of specific columns to factors

cols <- c("checking_balance", "credit_history", "purpose", "savings_balance", "employment_length","personal_status","other_debtors","property","installment_plan","housing","default","telephone","foreign_worker","job")

credit[,cols] <- lapply(credit[,cols],as.factor)

# Separation of objective variable from main dataframe

default <- credit$default
credit <- select(credit, -c(default))

# Logistic regression

credit$checking_balance <- factor(credit$checking_balance)
glm.credit<- glm(default~., family=binomial, data=credit)
summary(glm.credit)
```

    ## 
    ## Call:
    ## glm(formula = default ~ ., family = binomial, data = credit)
    ## 
    ## Deviance Residuals: 
    ##     Min       1Q   Median       3Q      Max  
    ## -2.3410  -0.6994  -0.3752   0.7095   2.6116  
    ## 
    ## Coefficients:
    ##                                        Estimate Std. Error z value Pr(>|z|)    
    ## (Intercept)                          -2.666e+00  1.280e+00  -2.083 0.037226 *  
    ## checking_balance> 200 DM             -9.657e-01  3.692e-01  -2.616 0.008905 ** 
    ## checking_balance1 - 200 DM           -3.749e-01  2.179e-01  -1.720 0.085400 .  
    ## checking_balanceunknown              -1.712e+00  2.322e-01  -7.373 1.66e-13 ***
    ## months_loan_duration                  2.786e-02  9.296e-03   2.997 0.002724 ** 
    ## credit_historydelayed                 5.826e-01  3.345e-01   1.742 0.081540 .  
    ## credit_historyfully repaid            1.436e+00  4.399e-01   3.264 0.001099 ** 
    ## credit_historyfully repaid this bank  1.579e+00  4.381e-01   3.605 0.000312 ***
    ## credit_historyrepaid                  8.497e-01  2.587e-01   3.284 0.001022 ** 
    ## purposecar (new)                      7.401e-01  3.339e-01   2.216 0.026668 *  
    ## purposecar (used)                    -9.264e-01  4.409e-01  -2.101 0.035645 *  
    ## purposedomestic appliances            2.173e-01  8.041e-01   0.270 0.786976    
    ## purposeeducation                      7.764e-01  4.660e-01   1.666 0.095718 .  
    ## purposefurniture                     -5.152e-02  3.543e-01  -0.145 0.884391    
    ## purposeothers                        -7.487e-01  7.998e-01  -0.936 0.349202    
    ## purposeradio/tv                      -1.515e-01  3.370e-01  -0.450 0.653002    
    ## purposerepairs                        5.237e-01  5.933e-01   0.883 0.377428    
    ## purposeretraining                    -1.319e+00  1.233e+00  -1.070 0.284625    
    ## amount                                1.283e-04  4.444e-05   2.887 0.003894 ** 
    ## savings_balance> 1000 DM             -1.339e+00  5.249e-01  -2.551 0.010729 *  
    ## savings_balance101 - 500 DM          -3.577e-01  2.861e-01  -1.250 0.211130    
    ## savings_balance501 - 1000 DM         -3.761e-01  4.011e-01  -0.938 0.348476    
    ## savings_balanceunknown               -9.467e-01  2.625e-01  -3.607 0.000310 ***
    ## employment_length0 - 1 yrs            2.097e-01  2.947e-01   0.712 0.476718    
    ## employment_length1 - 4 yrs            9.379e-02  2.510e-01   0.374 0.708653    
    ## employment_length4 - 7 yrs           -5.544e-01  3.007e-01  -1.844 0.065230 .  
    ## employment_lengthunemployed           2.766e-01  4.134e-01   0.669 0.503410    
    ## installment_rate                      3.301e-01  8.828e-02   3.739 0.000185 ***
    ## personal_statusfemale                -2.755e-01  3.865e-01  -0.713 0.476040    
    ## personal_statusmarried male          -3.671e-01  4.537e-01  -0.809 0.418448    
    ## personal_statussingle male           -8.161e-01  3.799e-01  -2.148 0.031718 *  
    ## other_debtorsguarantor               -1.415e+00  5.685e-01  -2.488 0.012834 *  
    ## other_debtorsnone                    -4.360e-01  4.101e-01  -1.063 0.287700    
    ## residence_history                     4.776e-03  8.641e-02   0.055 0.955920    
    ## propertyother                        -8.690e-02  2.313e-01  -0.376 0.707115    
    ## propertyreal estate                  -2.814e-01  2.534e-01  -1.111 0.266630    
    ## propertyunknown/none                  4.490e-01  4.130e-01   1.087 0.277005    
    ## age                                  -1.454e-02  9.222e-03  -1.576 0.114982    
    ## installment_plannone                 -6.463e-01  2.391e-01  -2.703 0.006871 ** 
    ## installment_planstores               -1.232e-01  4.119e-01  -0.299 0.764878    
    ## housingown                            2.402e-01  4.503e-01   0.534 0.593687    
    ## housingrent                           6.839e-01  4.770e-01   1.434 0.151657    
    ## existing_credits                      2.721e-01  1.895e-01   1.436 0.151109    
    ## dependents1                           2.647e-01  2.492e-01   1.062 0.288249    
    ## telephoneyes                         -3.000e-01  2.013e-01  -1.491 0.136060    
    ## foreign_workeryes                     1.392e+00  6.258e-01   2.225 0.026095 *  
    ## jobskilled employee                   7.524e-02  2.845e-01   0.264 0.791419    
    ## jobunemployed non-resident           -4.795e-01  6.623e-01  -0.724 0.469086    
    ## jobunskilled resident                 5.666e-02  3.501e-01   0.162 0.871450    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## (Dispersion parameter for binomial family taken to be 1)
    ## 
    ##     Null deviance: 1221.73  on 999  degrees of freedom
    ## Residual deviance:  895.82  on 951  degrees of freedom
    ## AIC: 993.82
    ## 
    ## Number of Fisher Scoring iterations: 5

``` r
# Extraction of columns

cols <- summary(glm.credit)$coeff[-1, 4] < 0.1 
relevant.cols <- names(cols)[cols == TRUE]
print(relevant.cols)
```

    ##  [1] "checking_balance> 200 DM"            
    ##  [2] "checking_balance1 - 200 DM"          
    ##  [3] "checking_balanceunknown"             
    ##  [4] "months_loan_duration"                
    ##  [5] "credit_historydelayed"               
    ##  [6] "credit_historyfully repaid"          
    ##  [7] "credit_historyfully repaid this bank"
    ##  [8] "credit_historyrepaid"                
    ##  [9] "purposecar (new)"                    
    ## [10] "purposecar (used)"                   
    ## [11] "purposeeducation"                    
    ## [12] "amount"                              
    ## [13] "savings_balance> 1000 DM"            
    ## [14] "savings_balanceunknown"              
    ## [15] "employment_length4 - 7 yrs"          
    ## [16] "installment_rate"                    
    ## [17] "personal_statussingle male"          
    ## [18] "other_debtorsguarantor"              
    ## [19] "installment_plannone"                
    ## [20] "foreign_workeryes"

We now will feed Boruta with the predictors the logistical regression
has found relevant to further filter them.

``` r
cols_ <- c("checking_balance", "credit_history", "purpose", "savings_balance", "employment_length","personal_status","other_debtors","installment_plan","foreign_worker")

credit <- credit[c(cols_)]

# Boruta

boruta.credit <- Boruta(default~., data = credit, doTrace = 2)
```

``` r
print(boruta.credit)
```

    ## Boruta performed 68 iterations in 14.56361 secs.
    ##  7 attributes confirmed important: checking_balance, credit_history,
    ## foreign_worker, installment_plan, other_debtors and 2 more;
    ##  2 attributes confirmed unimportant: employment_length,
    ## personal_status;

``` r
par(mar=c(10,5,5,5)+.1)
plot(boruta.credit, xlab= "", las=3)
```

![](main_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

The Boruta method was employed to identify the most important variables
in the analysis. Its analysis is clear: we’ll take the variables it
flags as relevant and leave the rest out.

## 4. Decision tree

First, the data will be cleaned to retain only the relevant variables.

``` r
cols__ <- c("checking_balance", "credit_history", "purpose", "savings_balance","other_debtors","installment_plan","foreign_worker")

credit <- credit[c(cols__)] 
```

Next, a test-train model will be constructed, using 2/3 of the data for
training and 1/3 for testing.

``` r
set.seed(1432)
y <- default
x <- credit
```

The decision tree can now be generated.

``` r
split_prop <- 3
max_split<-floor(nrow(x)/split_prop)
tr_limit <- nrow(x)-max_split
ts_limit <- nrow(x)-max_split+1

trainx <- x[1:tr_limit,]
trainy <- y[1:tr_limit]
testx <- x[ts_limit+1:nrow(x),]
testy <- y[ts_limit+1:nrow(x)]

split_prop <- 3
indexes = sample(1:nrow(credit), size=floor(((split_prop-1)/split_prop)*nrow(credit)))
trainx<-x[indexes,]
trainy<-y[indexes]
testx<-x[-indexes,]
testy<-y[-indexes]

summary(testx)
```

    ##    checking_balance                credit_history       purpose  
    ##  < 0 DM    : 98     critical              :100    radio/tv  :96  
    ##  > 200 DM  : 26     delayed               : 27    car (new) :72  
    ##  1 - 200 DM: 90     fully repaid          : 17    furniture :64  
    ##  unknown   :120     fully repaid this bank: 17    car (used):39  
    ##                     repaid                :173    business  :31  
    ##                                                   education :19  
    ##                                                   (Other)   :13  
    ##       savings_balance      other_debtors installment_plan foreign_worker
    ##  < 100 DM     :205    co-applicant: 11   bank  : 50       no : 12       
    ##  > 1000 DM    : 16    guarantor   : 23   none  :265       yes:322       
    ##  101 - 500 DM : 37    none        :300   stores: 19                     
    ##  501 - 1000 DM: 24                                                      
    ##  unknown      : 52                                                      
    ##                                                                         
    ## 

``` r
summary(testy)
```

    ##   0   1 
    ## 221 113

``` r
summary(trainx)
```

    ##    checking_balance                credit_history       purpose   
    ##  < 0 DM    :176     critical              :193    radio/tv  :184  
    ##  > 200 DM  : 37     delayed               : 61    car (new) :162  
    ##  1 - 200 DM:179     fully repaid          : 23    furniture :117  
    ##  unknown   :274     fully repaid this bank: 32    business  : 66  
    ##                     repaid                :357    car (used): 64  
    ##                                                   education : 31  
    ##                                                   (Other)   : 42  
    ##       savings_balance      other_debtors installment_plan foreign_worker
    ##  < 100 DM     :398    co-applicant: 30   bank  : 89       no : 25       
    ##  > 1000 DM    : 32    guarantor   : 29   none  :549       yes:641       
    ##  101 - 500 DM : 66    none        :607   stores: 28                     
    ##  501 - 1000 DM: 39                                                      
    ##  unknown      :131                                                      
    ##                                                                         
    ## 

``` r
summary(trainy)
```

    ##   0   1 
    ## 479 187

``` r
trainy = as.factor(trainy)
model <- C50::C5.0(trainx, trainy,rules=TRUE )
summary(model)
```

    ## 
    ## Call:
    ## C5.0.default(x = trainx, y = trainy, rules = TRUE)
    ## 
    ## 
    ## C5.0 [Release 2.07 GPL Edition]      Fri Feb 03 11:28:27 2023
    ## -------------------------------
    ## 
    ## Class specified by attribute `outcome'
    ## 
    ## Read 666 cases (8 attributes) from undefined.data
    ## 
    ## Rules:
    ## 
    ## Rule 1: (18/1, lift 1.3)
    ##  credit_history = repaid
    ##  other_debtors = guarantor
    ##  ->  class 0  [0.900]
    ## 
    ## Rule 2: (311/38, lift 1.2)
    ##  checking_balance in {> 200 DM, unknown}
    ##  ->  class 0  [0.875]
    ## 
    ## Rule 3: (202/28, lift 1.2)
    ##  savings_balance in {> 1000 DM, 501 - 1000 DM, unknown}
    ##  ->  class 0  [0.858]
    ## 
    ## Rule 4: (555/136, lift 1.0)
    ##  credit_history in {critical, delayed, repaid}
    ##  other_debtors = none
    ##  ->  class 0  [0.754]
    ## 
    ## Rule 5: (5, lift 3.1)
    ##  checking_balance in {< 0 DM, 1 - 200 DM}
    ##  credit_history = critical
    ##  purpose in {education, repairs}
    ##  ->  class 1  [0.857]
    ## 
    ## Rule 6: (36/9, lift 2.6)
    ##  checking_balance in {< 0 DM, 1 - 200 DM}
    ##  credit_history in {fully repaid, fully repaid this bank}
    ##  savings_balance in {< 100 DM, 101 - 500 DM}
    ##  ->  class 1  [0.737]
    ## 
    ## Rule 7: (5/1, lift 2.5)
    ##  checking_balance in {< 0 DM, 1 - 200 DM}
    ##  credit_history = critical
    ##  savings_balance = < 100 DM
    ##  other_debtors = guarantor
    ##  ->  class 1  [0.714]
    ## 
    ## Rule 8: (82/33, lift 2.1)
    ##  checking_balance = < 0 DM
    ##  credit_history in {delayed, repaid}
    ##  savings_balance in {< 100 DM, 101 - 500 DM}
    ##  other_debtors = none
    ##  ->  class 1  [0.595]
    ## 
    ## Rule 9: (15/6, lift 2.1)
    ##  checking_balance in {< 0 DM, 1 - 200 DM}
    ##  savings_balance in {< 100 DM, 101 - 500 DM}
    ##  other_debtors = co-applicant
    ##  ->  class 1  [0.588]
    ## 
    ## Rule 10: (154/75, lift 1.8)
    ##  checking_balance in {< 0 DM, 1 - 200 DM}
    ##  credit_history in {delayed, repaid}
    ##  savings_balance in {< 100 DM, 101 - 500 DM}
    ##  other_debtors = none
    ##  ->  class 1  [0.513]
    ## 
    ## Default class: 0
    ## 
    ## 
    ## Evaluation on training data (666 cases):
    ## 
    ##          Rules     
    ##    ----------------
    ##      No      Errors
    ## 
    ##      10  143(21.5%)   <<
    ## 
    ## 
    ##     (a)   (b)    <-classified as
    ##    ----  ----
    ##     430    49    (a): class 0
    ##      94    93    (b): class 1
    ## 
    ## 
    ##  Attribute usage:
    ## 
    ##   92.19% credit_history
    ##   89.04% other_debtors
    ##   78.98% checking_balance
    ##   61.86% savings_balance
    ##    0.75% purpose
    ## 
    ## 
    ## Time: 0.0 secs

``` r
model <- C50::C5.0(trainx, trainy)
plot(model)
```

![](main_files/figure-gfm/unnamed-chunk-13-1.png)<!-- -->

The error rate obtained was 21.5%, with 143 incorrect classifications
out of 666 objects.

To evaluate the model’s accuracy, we will use the previously saved test
data set.

``` r
predicted_model <- predict( model, testx, type="class" )
print(sprintf("The tree's precission is: %.4f %%",100*sum(predicted_model == testy) / length(predicted_model)))
```

    ## [1] "The tree's precission is: 71.2575 %"

The confusion matrix is the following.

``` r
mat_conf<-table(testy,Predicted=predicted_model)
mat_conf
```

    ##      Predicted
    ## testy   0   1
    ##     0 194  27
    ##     1  69  44

## 5. Random Forest

Random Forest is an algorithm of supervised learning, which builds a
“forest” of decision trees, from a training set.

Next, we will show how this algorithm can apply to this dataset. I’ll
first try to find the optimal parameters with a quick tuning and then
run a random forest with them.

``` r
# First generic Random Forest

control <- trainControl(method="repeatedcv", number=10, repeats=3)
seed <- 72
metric <- "Accuracy"
set.seed(seed)
mtry <- sqrt(ncol(trainx))
tunegrid <- expand.grid(.mtry=mtry)
rf_default <- train(trainx, trainy, method="rf", metric=metric, tuneGrid=tunegrid, trControl=control)
print(rf_default)
```

    ## Random Forest 
    ## 
    ## 666 samples
    ##   7 predictor
    ##   2 classes: '0', '1' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold, repeated 3 times) 
    ## Summary of sample sizes: 600, 599, 600, 599, 599, 600, ... 
    ## Resampling results:
    ## 
    ##   Accuracy   Kappa    
    ##   0.7454216  0.3141934
    ## 
    ## Tuning parameter 'mtry' was held constant at a value of 2.645751

``` r
# Random Search

control <- trainControl(method="repeatedcv", number=10, repeats=3, search="random")
set.seed(seed)
mtry <- sqrt(ncol(trainx))
rf_random <- train(trainx, trainy, method="rf", metric=metric, tuneLength=7, trControl=control)
print(rf_random)
```

    ## Random Forest 
    ## 
    ## 666 samples
    ##   7 predictor
    ##   2 classes: '0', '1' 
    ## 
    ## No pre-processing
    ## Resampling: Cross-Validated (10 fold, repeated 3 times) 
    ## Summary of sample sizes: 600, 599, 600, 599, 599, 600, ... 
    ## Resampling results across tuning parameters:
    ## 
    ##   mtry  Accuracy   Kappa    
    ##   2     0.7544065  0.3211048
    ##   3     0.7439291  0.3118263
    ##   4     0.7393756  0.3020379
    ##   5     0.7373856  0.3015154
    ##   7     0.7309259  0.2784969
    ## 
    ## Accuracy was used to select the optimal model using the largest value.
    ## The final value used for the model was mtry = 2.

``` r
plot(rf_random)
```

![](main_files/figure-gfm/unnamed-chunk-17-1.png)<!-- -->

``` r
# Random Forest

rf <- randomForest(trainx, trainy, mtry = 2)
predicted_rf <- predict(rf, testx, type="class" )
print(sprintf("Random forest's accuracy is: %.4f %%",100*sum(predicted_rf == testy) / length(predicted_rf)))
```

    ## [1] "Random forest's accuracy is: 70.0599 %"

## 6. Naive Bayes

We will use a Naive-Bayes approach, which is a variation of the
classical decision tree. It works as follows.

``` r
modelb<-naiveBayes(trainx, trainy, proximity=T)
modelb
```

    ## 
    ## Naive Bayes Classifier for Discrete Predictors
    ## 
    ## Call:
    ## naiveBayes.default(x = trainx, y = trainy, proximity = T)
    ## 
    ## A-priori probabilities:
    ## trainy
    ##         0         1 
    ## 0.7192192 0.2807808 
    ## 
    ## Conditional probabilities:
    ##       checking_balance
    ## trainy     < 0 DM   > 200 DM 1 - 200 DM    unknown
    ##      0 0.18371608 0.06263048 0.24634656 0.50730689
    ##      1 0.47058824 0.03743316 0.32620321 0.16577540
    ## 
    ##       credit_history
    ## trainy   critical    delayed fully repaid fully repaid this bank     repaid
    ##      0 0.33820459 0.09185804   0.01461378             0.02922756 0.52609603
    ##      1 0.16577540 0.09090909   0.08556150             0.09625668 0.56149733
    ## 
    ##       purpose
    ## trainy    business   car (new)  car (used) domestic appliances   education
    ##      0 0.083507307 0.223382046 0.116910230         0.014613779 0.037578288
    ##      1 0.139037433 0.294117647 0.042780749         0.021390374 0.069518717
    ##       purpose
    ## trainy   furniture      others    radio/tv     repairs  retraining
    ##      0 0.181628392 0.012526096 0.296450939 0.018789144 0.014613779
    ##      1 0.160427807 0.010695187 0.224598930 0.032085561 0.005347594
    ## 
    ##       savings_balance
    ## trainy   < 100 DM  > 1000 DM 101 - 500 DM 501 - 1000 DM    unknown
    ##      0 0.54906054 0.06054280   0.08768267    0.06889353 0.23382046
    ##      1 0.72192513 0.01604278   0.12834225    0.03208556 0.10160428
    ## 
    ##       other_debtors
    ## trainy co-applicant  guarantor       none
    ##      0   0.03757829 0.04592902 0.91649269
    ##      1   0.06417112 0.03743316 0.89839572
    ## 
    ##       installment_plan
    ## trainy       bank       none     stores
    ##      0 0.11482255 0.85594990 0.02922756
    ##      1 0.18181818 0.74331551 0.07486631
    ## 
    ##       foreign_worker
    ## trainy         no        yes
    ##      0 0.04801670 0.95198330
    ##      1 0.01069519 0.98930481

``` r
predicted_model2 <- predict(modelb, testx, type="class" )
print(sprintf("The Bayesian Model's accuracy is: %.4f %%",100*sum(predicted_model2 == testy) / length(predicted_model2)))
```

    ## [1] "The Bayesian Model's accuracy is: 71.2575 %"

``` r
mat_conf2<-table(testy,Predicted=predicted_model2)
mat_conf2
```

    ##      Predicted
    ## testy   0   1
    ##     0 191  30
    ##     1  66  47

## 7. Logistic regression(prediction)

We will use now a logistic regression for prediction.

``` r
log_pred <- glm(trainy~., family=binomial, data=trainx)

# Predicting
pred_prob <- predict(log_pred, testx, type = "response")

# Converting from probability to actual output
test_actual <- ifelse(pred_prob >= 0.5, 1, 0)
# Generating the classification table
conf_mat <- table(testy, test_actual)
conf_mat
```

    ##      test_actual
    ## testy   0   1
    ##     0 197  24
    ##     1  72  41

``` r
# Accuracy

accuracy <- sum(diag(conf_mat))/sum(conf_mat)*100
print(sprintf("Logistic regression's accuracy is: %.4f %%", accuracy))
```

    ## [1] "Logistic regression's accuracy is: 71.2575 %"

## 8. Conclusions

-   The 4 models give a pretty similar accuracy, of around 70%. Other
    machine learning projects seen using the same dataset have a very
    similar indicator, so it can be assumed this is about the maximum
    accuracy we can get from applying this type of models.

-   To boost the indicators of any future Machine Learning project using
    this dataset, some measures can be implemented, such as the
    numerization and scaling of the different columns to test other
    edge-cutting algorithms suchg as LightGBM or neural networks. If the
    same cathegorical approach is followed (as in this project),
    bootstrapping could be an interesting approach as well.

-   Another approach to the problem could be to deal with it as an
    unsupervised Machine Learning project, get some clusters and try to
    make predictions and association rules out of them with the
    algorithms here tried.

## 9. Bibliography

We get ideas for this analysis from the following sites.

-   <https://www.r-bloggers.com/2018/01/understanding-naive-bayes-classifier-using-r/>

-   <https://www.youtube.com/watch?v=6EXPYzbfLCE&t=786s>

-   <https://machinelearningmastery.com/tune-machine-learning-algorithms-in-r/>

-   <https://thinkingneuron.com/german-credit-risk-classification-case-study-in-python/>
