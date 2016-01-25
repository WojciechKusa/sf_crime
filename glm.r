setwd("C:/Users/Wojtek/OneDrive/STUDIA/Eksploracja danych/projekt/sf_crime")



library(randomForest)

library(MASS)
library(readr)
#library (rpart)
library(caret)
library(lubridate)

explore<-function(x){
  barplot(table(x),horiz=T,cex.names=0.7,las=2)
}

treatment<-function(fname){
  df<-read.csv(paste0('./input/',fname))
  #df<-read_csv(paste0('../input/',fname))
  Dates1  = strptime(as.character(df$Dates),"%Y-%m-%d %H:%M:%S")
  print(str(Dates1))
  df$Year = Dates1$year
  df$Month = Dates1$mon
  df$Hour = as.numeric(format(ymd_hms(Dates1), "%H"))
  df$Minute<- minute(ymd_hms(df$Dates))
  df$Time <- df$Hour * 60 + df$Minute
  #df$Loc = paste0('(',round(df$X,2),',',round(df$Y,2),')')
  df$Loc = as.factor(paste(round(df$X,2), round(df$Y,2), sep= " "))
  df$XY <- -df$X * df$Y	
  df$XandY <- -df$X + df$Y
  df$DayOfWeekHour <- as.numeric(df$DayOfWeek) * df$Hour
  df$DayOfWeekandHour <- as.numeric(df$DayOfWeek) + df$Hour
  df$AddOf <- sapply(df$Address, FUN=function(x) {strsplit(as.character(x), split="of ")[[1]][2]})
  df$AddType <- as.factor(ifelse(is.na(df$AddOf ),1,2))
  df$DistrictAndTime <- as.numeric(df$PdDistrict) + df$Hour 
  df$DistrictTime <- as.numeric(df$PdDistrict) * df$Hour
    return(df)
}


train<-treatment('train.csv')
print(str(train))
print('Read train data complete...')
test<-treatment('test.csv')
print('Read test data complete...')
#District and Locations are explored with significnat impact on type of crime
#explore(train$PdDistrict)
#explore(train$Loc)

##split train data into 10 paritions due to memory space constraint

inTrain<-createDataPartition(train$Category,p=0.85,list=F)
train.sub<-train[inTrain,]

#rm(submission)


## create raprt training model
rpart.train<-function(train,test){
  submission<-data.frame(Id=test$Id)
  response<-data.frame(Cat=train$Category)
  #extract the names of crime
  crime<-as.character(unique(train$Category))
  crime<-sort(crime)
  for (i in crime){
    #i = 'ASSAULT'
    response[i]<- 0
    response[i][response$Cat==i,]<- 1
    fit<-glm(response[,i] ~ PdDistrict + X + Y + XY + XandY +DayOfWeek+Year+Time+ Hour+Month + 
             AddType + DayOfWeekHour + DayOfWeekandHour + DistrictAndTime + DistrictTime,
             data = train, 
             family = binomial)
    pred <- predict(fit,test, type = "response")
    submission[i]<-pred
    print(paste0(ncol(submission)/length(crime)*100,'% completed'))
  }
  return(submission)
}
submission<-rpart.train(train,test)

write.csv(submission,'submission.csv',row.names=F)
gz_out <- gzfile("submit_1.csv.gz", "w")
writeChar(format_csv(submission, ""), gz_out, eos=NULL)
close(gz_out)

#rm(train, test,train.sub)


final_submission <- as.data.frame(ifelse(apply(submission[,2:40],1,max) == submission[,2:40], 1, 0))


final_submission <- cbind(submission[,1], final_submission)
names(final_submission)[1] <- "Id"

gz_out <- gzfile("submit.csv.gz", "w")
writeChar(format_csv(final_submission, ""), gz_out, eos=NULL)
close(gz_out)


nonzero <- function(x) sum(x != 0)
crimes_histogram_test <- numcolwise(nonzero)(final_submission)
crimes_histogram_test <- crimes_histogram_test[-1]

