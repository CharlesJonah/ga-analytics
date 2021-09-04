# Query for Part 1, Question 1
GET_ALL_SESSIONS = """SELECT SUM(DerivedTable.maxVisitNumber) FROM (SELECT fullvisitorid, MAX(visitNumber) as maxVisitNumber 
FROM GoogleAnalyticsSample.ga_sessions_export GROUP BY fullvisitorid) AS DerivedTable"""

# Query for part 1, Question 2
SESSIONS_PER_USER = """SELECT fullvisitorid, MAX(visitNumber) as maxVisitNumber FROM GoogleAnalyticsSample.ga_sessions_export GROUP BY fullvisitorid"""

# Query for part 1, Question 2
TIME_TO_ORDER_CONFIRMATION = """SELECT AVG(hit_level_one.element.time) AS average_time_to_order_confirmation
FROM GoogleAnalyticsSample.ga_sessions_export, UNNEST(hit.list) as hit_level_one, 
UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two  WHERE hit_level_two.element.value='order_confirmation'"""
