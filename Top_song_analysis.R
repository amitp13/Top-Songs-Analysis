library(dplyr)
library(tidyr)
library(ggplot2)
library(plyr)
library(lubridate)
library(factoextra)
library(psych)
library(NbClust)
library(reshape2)
library(wordcloud2)
library(dbscan)
library(fpc)
spotify <- read.csv("C:\\Users\\phadk\\Desktop\\Work\\projects\\Top-Songs-Analysis\\songs.csv",header = TRUE)
Data <- spotify

#----------------------------DATA CLEANING -------------------------------- #
dim(Data)  #getting rows and columns
summary(Data) #summary of entire data

colSums(is.na(Data)) #finding missing data

#since we have no missing data lets clean up our dataset further.

#Convert ms to secs 
Data$duration_ms <- Data$duration_ms/1000 
colnames(Data)[3]<-"duration_s"

#scaling our audio properties data 
Data[,c(6:14)] <- scale(Data[,c(6:14)])


#-----------------------------Exploratory Data Analysis-------------------------------------------#

#Most frequent artist available in dataset
artist_freq <- count(Data, 'artist')
wordcloud2(data = artist_freq)

#range of a duration of songs in dataset
qplot(seq_along(Data$duration_s), Data$duration_s,  main = "Duration of Songs",
      xlab = 'Seconds',
      ylab = 'No. of songs',)

x <- as.factor(Data$mode)
ggplot(Data, aes(x= Data$mode)) + geom_bar(size=2)

mode_freq <- count(Data,'mode')
mode_freq$mode[mode_freq$mode == 0] <- "Minor"
mode_freq$mode[mode_freq$mode == 1] <- "Major"
barplot(height=mode_freq$freq, names=mode_freq$mode, 
        col=rgb(0.8,0.1,0.1,0.6),
        xlab="mode", 
        ylab="frequency", 
        main="Modality of songs", 
)

#Plotting audio properties on a histogram
ap <- melt(Data[,c(6:12)])
ggplot(ap,aes(x = value)) + 
  facet_wrap(~variable,scales = "free_x") + 
  geom_histogram() 


#-----------------------------Principal Component Analysis------------------------------------------#

data.pca = Data[,c(6:12)]   #taking out only audio properties variables
pca <- prcomp(data.pca, scale=TRUE, center=TRUE)
summary(pca)

pca$rotation
fviz_screeplot(pca, type='bar',main='Scree plot')

fviz_pca_biplot(pca,
                col.var = "#2E9FDF", # Variables color
                col.ind = "#696969"  # Individuals color
                )
#-------------------------------------Clustering --------------------------------------------#
# split data into train and test
# Lets take a sample of 75/25 like before. Dplyr preserves class.
data_sample <- Data[sample(nrow(Data),20553),]
training_sample <- sample(c(TRUE, FALSE), nrow(data_sample), replace = T, prob = c(0.75,0.2))
train <- data_sample[training_sample, ]
test <- data_sample[!training_sample, ]



#Kmeans Clustering: Centroid Based
fviz_nbclust(train_ap, kmeans, method="silhouette")
fviz_nbclust(train_ap, kmeans, method="wss") + geom_vline(xintercept = 4, linetype=2)

#according to wss and silhouette method we see that optimal k is 4 or 2. Thus assuming k as 4
set.seed(1234)
clusters4 <- kmeans(train_ap, 4)
fviz_cluster(clusters4, data = train_ap,
             palette = c("#2E9FDF", "#00AFBB", "#E7B800", "#32CD32"), 
             geom = "point",
             ellipse.type = "convex", 
             ggtheme = theme_bw()
)

#Assuming k as 3
set.seed(123)
clusters3 <- kmeans(train_ap, 3)
fviz_cluster(clusters3, data = train_ap,
             geom = "point",
             ellipse.type = "convex", 
             ggtheme = theme_bw()
)

#Clustering based on heirarchy
set.seed(123)
distances <- dist(train[,c(5,6,7,9,10,13)],method="euclidean")
hcluster <- hclust(distances, method="ward")
plot(hcluster)
cluster_groups <- cutree(hcluster, k=4)
tapply(train$danceability, cluster_groups,mean)
tapply(train$energy, cluster_groups,mean)
tapply(train$loudness, cluster_groups,mean)
tapply(train$acousticness, cluster_groups,mean)
tapply(train$instrumentalness, cluster_groups,mean)
tapply(train$valence, cluster_groups,mean)
#Here we see 4 cluster seem the best options.
#Cluster 1 : highly acoustic and instrumental songs with very low mood or minor modality. Probably classical or slow rnB  
#Cluster 2 : acoustic songs with major chords and bit of high tempo.
#Cluster 3 : high energy songs with low dancebility, probably hard rock or rock songs
#Cluster 4 : happy sounding songs with high energy and highly danceability
cluster_groups
clusters <- data.frame(hcluster$order)

train_w_clusters = cbind(train, cluster_groups)

# Recomending similar songs to 	Otis reddings' Pain In My Heart
subset(train_w_clusters,track=="Pain In My Heart" )

cluster_no1 <- subset(train_w_clusters, cluster_groups==1)
cluster_no1[1:25,c(1,2)]

