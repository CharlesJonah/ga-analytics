# Query for Part 1, Question 1
GET_ALL_SESSIONS = """
SELECT SUM(DerivedTable.maxVisitNumber) FROM (SELECT fullvisitorid, MAX(visitNumber) as maxVisitNumber 
FROM GoogleAnalyticsSample.ga_sessions_export GROUP BY fullvisitorid) AS DerivedTable
"""

# Query for part 1, Question 2
SESSIONS_PER_USER = """
SELECT fullvisitorid, MAX(visitNumber) as maxVisitNumber FROM GoogleAnalyticsSample.ga_sessions_export 
GROUP BY fullvisitorid ORDER BY fullVisitorId  LIMIT {0} OFFSET {1}
"""

# Query for part 1, Question 3
TIME_TO_ORDER_CONFIRMATION = """
SELECT AVG(hit_level_one.element.time) AS average_time_to_order_confirmation
FROM GoogleAnalyticsSample.ga_sessions_export, UNNEST(hit.list) as hit_level_one, 
UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two  WHERE hit_level_two.element.value='order_confirmation'
"""
# Query for part 1, Question 4(a)
CALCULATE_COORDINATES_CHANGE = """
SELECT *, 
    ST_DISTANCE(
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longStart AS FLOAT64 ), SAFE_CAST(visitor_locations.latStart AS FLOAT64)),
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longEnd AS FLOAT64 ), SAFE_CAST(visitor_locations.latEnd AS FLOAT64))
    ) as coordinatesChange
FROM
    (
        SELECT fullVisitorId, visitNumber, visitId,
        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='home') OR (hit_level_two.element.value='listing')
        ) [SAFE_OFFSET(0)] AS screenTypeStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        ) [SAFE_OFFSET(0)] AS latStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        ) [SAFE_OFFSET(0)] AS longStart,

        ARRAY_REVERSE(ARRAY ( SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='order_placement') OR (hit_level_two.element.value='checkout')
        )) [SAFE_OFFSET(0)] AS screenTypeEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        )) [SAFE_OFFSET(0)] AS latEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        )) [SAFE_OFFSET(0)] AS longEnd,

        FROM GoogleAnalyticsSample.ga_sessions_export LIMIT {0} OFFSET {1}
    ) AS visitor_locations
"""

# Query for part 1, Question 4(b)
ORDER_PLACED_IF_CUSTOMER_CHANGED_LOCATION = """
SELECT visitor_locations_with_distances.*, transactional_data.* FROM
(SELECT *, 
    ST_ASTEXT(ST_GEOGPOINT(SAFE_CAST(visitor_locations.longEnd AS FLOAT64 ), SAFE_CAST(visitor_locations.latEnd AS FLOAT64))) as last_location,
    ST_DISTANCE(
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longStart AS FLOAT64 ), SAFE_CAST(visitor_locations.latStart AS FLOAT64)),
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longEnd AS FLOAT64 ), SAFE_CAST(visitor_locations.latEnd AS FLOAT64))
    ) as coordinatesChange
FROM
    (
        SELECT fullVisitorId, visitNumber, visitId, SAFE_CAST(date AS STRING) AS date,
        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='home') OR (hit_level_two.element.value='listing')
        ) [SAFE_OFFSET(0)] AS screenTypeStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        ) [SAFE_OFFSET(0)] AS latStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        ) [SAFE_OFFSET(0)] AS longStart,

        ARRAY_REVERSE(ARRAY ( SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='order_placement') OR (hit_level_two.element.value='checkout')
        )) [SAFE_OFFSET(0)] AS screenTypeEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        )) [SAFE_OFFSET(0)] AS latEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        )) [SAFE_OFFSET(0)] AS longEnd,

        FROM GoogleAnalyticsSample.ga_sessions_export
    ) AS visitor_locations
) AS visitor_locations_with_distances
LEFT JOIN
BackendDataSample.transactionalData AS transactional_data
ON visitor_locations_with_distances.last_location = transactional_data.geopointCustomer
WHERE (visitor_locations_with_distances.date=REPLACE(SAFE_CAST(transactional_data.orderDate AS STRING), '-', ''))
AND visitor_locations_with_distances.coordinatesChange > 0
ORDER BY visitor_locations_with_distances.fullVisitorId LIMIT {0} OFFSET {1}
"""

# Part 2
ORDER_PLACED_PER_VISITOR_ID = """
SELECT visitor_locations_with_distances.*, transactional_data.* FROM
(SELECT *, 
    ST_ASTEXT(ST_GEOGPOINT(SAFE_CAST(visitor_locations.longEnd AS FLOAT64 ), SAFE_CAST(visitor_locations.latEnd AS FLOAT64))) as last_location,
    ST_DISTANCE(
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longStart AS FLOAT64 ), SAFE_CAST(visitor_locations.latStart AS FLOAT64)),
        ST_GEOGPOINT(SAFE_CAST(visitor_locations.longEnd AS FLOAT64 ), SAFE_CAST(visitor_locations.latEnd AS FLOAT64))
    ) as coordinatesChange
FROM
    (
        SELECT fullVisitorId, visitNumber, visitId, SAFE_CAST(date AS STRING) AS date, operatingSystem,
        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='home') OR (hit_level_two.element.value='listing')
        ) [SAFE_OFFSET(0)] AS screenTypeStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        ) [SAFE_OFFSET(0)] AS latStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        ) [SAFE_OFFSET(0)] AS longStart,

        ARRAY_REVERSE(ARRAY ( SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE (hit_level_two.element.value='order_placement') OR (hit_level_two.element.value='checkout')
        )) [SAFE_OFFSET(0)] AS screenTypeEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=19
        )) [SAFE_OFFSET(0)] AS latEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=18
        )) [SAFE_OFFSET(0)] AS longEnd,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=16
        ) [SAFE_OFFSET(0)] AS cityStart,

        ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=15
        ) [SAFE_OFFSET(0)] AS countryStart,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=16
        )) [SAFE_OFFSET(0)] AS cityEnd,

        ARRAY_REVERSE(ARRAY (SELECT hit_level_two.element.value
        FROM UNNEST(hit.list) as hit_level_one, UNNEST(hit_level_one.element.customDimensions.list) as hit_level_two 
        WHERE hit_level_two.element.index=15
        )) [SAFE_OFFSET(0)] AS countryEnd,

        

        FROM GoogleAnalyticsSample.ga_sessions_export
    ) AS visitor_locations
) AS visitor_locations_with_distances
LEFT JOIN
BackendDataSample.transactionalData AS transactional_data
ON visitor_locations_with_distances.last_location = transactional_data.geopointCustomer
WHERE (visitor_locations_with_distances.date=REPLACE(SAFE_CAST(transactional_data.orderDate AS STRING), '-', ''))
AND (visitor_locations_with_distances.fullVisitorId='{0}')
"""
