library(readr)
library(dplyr)
library(ggplot2)
library(ggridges)
library(highcharter)
library(plyr)
library(lubridate)
library(fmsb)
library(gridExtra)
library(cmna)
library(tidyselect)
library(factoextra)
library(psych)
library(gvlma)
library(MASS)
library(NbClust)
library(GGally)
library(car)
library(reshape2)
spotify <- read.csv("C:\\Users\\phadk\\Desktop\\Work\\projects\\Top-Songs-Analysis\\songs.csv",header = TRUE)
View(spotify)
Data <- spotify

#----------------------------DATA CLEANING -------------------------------- #

#finding missing data
dim(Data)
colSums(is.na(Data))

#removing uneccesary columns
Data$id <- NULL
Data$year <- NULL
Data$key <- NULL
Data$duration_ms <- NULL
#speechiness also include podcast and speeches
#For songs speechiness will be low and inaccurate, hence removing spch

#Normalizing Loudness
range01 <- function(x){(x-min(x))/(max(x)-min(x))}

Data$loudness <- range01(Data$loudness)
Data$tempo <- range01(Data$tempo)
Data$instrumentalness <- range01(Data$instrumentalness)
summary(Data)



#-----------------------------Exploratory Data Analysis-------------------------------------------#
d <- melt(Data[,c(5:13)])
ggplot(d,aes(x = value)) + 
  facet_wrap(~variable,scales = "free_x") + 
  geom_histogram()

x <- as.factor(Data$mode)
ggplot(Data, aes(x= Data$mode)) + 
  geom_bar(size=2)

#From our analysis we se most of the audio props are normally distributed. 
#There is a big difference in mode. Songs with mode 1 dominate so it might skew our cluster analysis.  

data.pca = Data[,c(5:13)]   #taking out only numeric variables
pca <- prcomp(data.pca, scale=TRUE, center=TRUE)
summary(pca)

pca$rotation
fviz_screeplot(pca, type='bar',main='Scree plot')

fviz_pca_biplot(pca,
                col.var = "#2E9FDF", # Variables color
                col.ind = "#696969"  # Individuals color
                )
#-------------------------------------Splitting Dataset--------------------------------------#
# split data into train and test
# Lets take a sample of 75/25 like before. Dplyr preserves class.
training_sample <- sample(c(TRUE, FALSE), nrow(Data), replace = T, prob = c(0.75,0.25))
train <- Data[training_sample, ]
test <- Data[!training_sample, ]
#--------------------------------------K Means Clustering------------------------------------#
#scaling the data and finding generalized euclidean distance
View(train)
train.num <- Data[,c(5,8,9,10,11)]
scale_data = scale(train.num)
View(scale_data)
#To validate our assumption we took the help of the nbclust function t find optimal no. of clusters
fviz_nbclust(scale_data, kmeans, method='silhouette') #using silhoutte

#As per our analysis we can assume that K = 3
set.seed(101)
kmeans4 <- kmeans(train.num,4,nstart=25)

kmeans4$size

fviz_cluster(kmeans4,data=scale_data,
             geom = "point",
             ggtheme = theme_bw())

set.seed(101)
kmeans3 <- kmeans(train.num,3,nstart=25)

kmeans3$size

fviz_cluster(kmeans3,data=scale_data,
             geom = "point",
             ggtheme = theme_bw())


kmeans3$centers