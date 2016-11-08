rm(list = ls())
library(reshape2)
library(stringr)
# read data file
setwd("E:/backup/GoogleDrive/py/scrapy/flashscore/atp-singles")
stats = read.csv("stats.csv", header = TRUE)

# remove index var
stats = stats[,-1]

# base var
base = cbind.data.frame(stats["tournament_name"], stats["winner"], stats["time"])
base = rbind.data.frame(base, base)

# player A stats
pA = cbind.data.frame(stats["playerA"], stats["atp_A"], stats["scoreA"], stats["oddsA"], stats["acesA"], stats["dfA"], stats["fsppA"], stats["fspA"],
                      stats["sspA"], stats["bpsA"], stats["frpA"], stats["srpA"], stats["bpcA"], stats["mprA"], stats["spwA"], stats["rpwA"], stats["tpwA"],
                      stats["mgrA"], stats["sgwA"], stats["rgwA"], stats["tgwA"])
# player B stats
pB = cbind.data.frame(stats["playerB"], stats["atp_B"], stats["scoreB"], stats["oddsB"], stats["acesB"], stats["dfB"], stats["fsppB"], stats["fspB"],
                      stats["sspB"], stats["bpsB"], stats["frpB"], stats["srpB"], stats["bpcB"], stats["mprB"], stats["spwB"], stats["rpwB"], stats["tpwB"],
                      stats["mgrB"], stats["sgwB"], stats["rgwB"], stats["tgwB"])

# rename col names for merging
colnames(pB) = names(pA)

# row bind playerA & playerB stats
statsAB = rbind.data.frame(pA, pB)

# remove "-" from Odds var
statsAB$odd[statsAB$odd == '-'] <- NA

# split to get numeric stats
num_stats = data.frame(lapply(statsAB[,c(8:13, 15:17, 19:21)], as.character), stringsAsFactors=FALSE)

table = 1:length(num_stats$fspA)
for(i in 1:ncol(num_stats)){
  num = data.frame(do.call('rbind', strsplit(num_stats[,i], '%', fixed=TRUE))[,1])
  table = cbind(table, num)
}

# add stats that have one numeric value
nosplit = statsAB[,c(1:7, 14, 18)]  

# convert data types
base = data.frame(lapply(base, as.character), stringsAsFactors = FALSE)
num_stats = data.frame(lapply(table[,-1],function(x) as.numeric(levels(x))[x]))

# remove "-" from Odds variable
levels(nosplit$oddsA) = sub("-", "", levels(nosplit$oddsA))

# stack by columns
table = cbind(base, nosplit, num_stats)

# table columns names
nm = c("tournament_name", "winner", "time", "player", "atp", "score",
       "odds", "aces", "df", "fspp", "fsp", "ssp", "bps", "mpr", "frp",
       "srp", "bpc", "spw", "rpw", "tpw", "mgr", "sgw", "rgw", "tgw")
colnames(table) = nm

# rename Winner variable values from A win B win to 1 and 0
table$winner[table$winner == "A win"] <- 1; table$winner[table$winner == "B win"] <- 0

# extract tennis court
start_pos = regexpr(",", table$tournament_name)
stop_pos = regexpr(" -", table$tournament_name)

need = cbind(table$tournament_name, start_pos, stop_pos)
res = NULL
for(i in 1:length(need[,1])){
  if(start_pos[i]!=0 && stop_pos[i] !=0){
    row = substr(need[,1][i], start_pos[i], stop_pos[i])
    row = gsub(", ","", row)
  }
  else{
    row = ""
  }
  res = rbind(res, row)
}

table$tournament_court = gsub(" ", "", matrix(unlist(res), nrow=length(res), byrow=T))

# save results
write.table(table, file = "table.csv", sep = ",", row.names = FALSE)

# remove all except table
rm(list= ls()[!(ls() %in% c('table'))])
