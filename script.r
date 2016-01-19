#setwd("C:/Users/Wojtek/OneDrive/STUDIA/Eksploracja danych/projekt/sf_crime")

#this.dir <- dirname(parent.frame(2)$ofile)
#setwd(this.dir)

train <- read.csv("./input/train.csv")
test <- read.csv("./input/test.csv")

library(lubridate)
library(dplyr)
library(ggmap)
library(ggplot2)
library(readr)

train$Year <- year(ymd_hms(train$Dates))

train$Month<- month(ymd_hms(train$Dates))

train$Day<- day(ymd_hms(train$Dates))

train$Hour<- hour(ymd_hms(train$Dates))

train$Minute<- minute(ymd_hms(train$Dates))

train$Second<- second(ymd_hms(train$Dates))


map<-get_map(location="sanfrancisco",zoom=12,source="osm")

p <- ggmap(map) +
  geom_point(data=train, aes(x=X, y=Y, color=factor(PdDistrict)), alpha=0.05) +
  guides(colour = guide_legend(override.aes = list(alpha=1.0, size=6.0),
                               title="PdDistrict")) +
  scale_colour_brewer(type="qual",palette="Paired") + 
  ggtitle("Map of PdDistricts") +
  theme_light(base_size=20) +
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank())


ggsave("sf_districts_map.png", p, width=14, height=10, units="in")


