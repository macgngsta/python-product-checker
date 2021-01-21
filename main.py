from checker.checker import Checker
from checker.strategy.kaiser_norcal_strategy import KaiserNorCal

check = Checker()
#add strategy
knc_strat = KaiserNorCal()
knc_strat.facilities=['SFO','SSF']
check.add_strategy(knc_strat)

#start executing
check.execute()