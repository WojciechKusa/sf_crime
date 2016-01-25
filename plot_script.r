setwd("C:/Users/Wojtek/OneDrive/STUDIA/Eksploracja danych/projekt/sf_crime")

library(lubridate)
library(dplyr)
library(plyr)
library(ggmap)
library(ggplot2)
library(readr)

library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)


train <- read.csv('./input/train.csv')

map<-get_map(location="sanfrancisco",zoom=12,source="osm")

p <- ggmap(map) +
  geom_point(data=train, aes(x=X, y=Y, color=factor(PdDistrict)), alpha=0.05) +
  guides(colour = guide_legend(override.aes = list(alpha=1.0, size=6.0),
                               title="Posterunki policji")) +
  scale_colour_brewer(type="qual",palette="Paired") + 
  ggtitle("Mapa dystryktów podzielona ze wzglêdu na posterunki policji") +
  theme_light(base_size=20) +
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank())


ggsave("sf_districts.png", p, width=14, height=10, units="in")


train.sub <- subset(train ,  Category == "DRUG/NARCOTIC" | Category == "SEX OFFENSES FORCIBLE")

c <- ggmap(map) +
  geom_point(data=train.sub, aes(x=X, y=Y, color=factor(Category)), alpha=0.7) +
  guides(colour = guide_legend(override.aes = list(alpha=1.0, size=6.0),
                               title="Rodzaj przestêpstwa")) +
  scale_colour_brewer(type="qual") + 
  ggtitle("Mapa dystryktów podzielona ze wzglêdu na przestêpstwa") +
  theme_light(base_size=20) +
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank())

ggsave("sf_crimes_1.png", c, width=14, height=10, units="in")



train.top8 <- subset(train ,  Category == "LARCENY/THEFT"| Category == "ASSAULT"| Category == "DRUG/NARCOTIC"
                      | Category == "MISSING PERSON" | Category == "WARRANTS" | Category == "VEHICLE THEFT"
                      | Category == "VANDALISM" | Category == "BURGLARY")

c <- ggmap(map) +
  geom_point(data=train.top8, aes(x=X, y=Y, color=factor(Category)), alpha=0.05) +
  guides(colour = guide_legend(override.aes = list(alpha=1.0, size=6.0),
                               title="Rodzaj przestêpstwa")) +
  scale_colour_brewer(type="qual",palette="Paired") + 
  ggtitle("Mapa dystryktów podzielona ze wzglêdu na przestêpstwa dla top 8 przestêpstw.") +
  theme_light(base_size=20) +
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank())


ggsave("sf_crimes_all.png", c, width=14, height=10, units="in")


