andrew_bdm from leadlist 
import LeadList from leadsource 
import LeadSource from top100prospectleads 
import Top100ProspectLeads from top10targetsfortheweek 
import Top10TargetsForTheWeek from todaysactivity 
import TodaysActivity 
from TodayTarget import TodayTarget 
from game_loop import GameLoop 
from bant import BANT

leads = LeadList("sales_leads.csv") 
top_leads = Top100ProspectLeads() 
top_leads.add_leads(leads.process_leads()) 
top_10_targets = Top10TargetsForTheWeek() 
top_10_targets.add_leads(top_leads.get_leads()) 
today_target = TodayTarget(top_10_targets.get_leads()) 
todays_activity = TodaysActivity() 
bant = BANT() game_loop = GameLoop(today_target, todays_activity, bant) 
game_loop.start()