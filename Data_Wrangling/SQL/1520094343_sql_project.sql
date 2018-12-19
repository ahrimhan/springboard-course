/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */

/* Submitted by Ahrim Han on 12/1/2018 */


/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */

SELECT name
FROM Facilities
WHERE membercost > 0

/* Q2: How many facilities do not charge a fee to members? */

SELECT COUNT(name) AS count_no_member_cost
FROM Facilities
WHERE membercost = 0

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

SELECT facid, name, membercost, monthlymaintenance
FROM Facilities
WHERE membercost < monthlymaintenance * 0.2

/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */

SELECT *
FROM Facilities
WHERE facid IN (1, 5)

/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */

SELECT name, monthlymaintenance,
  CASE WHEN monthlymaintenance > 100 THEN 'expensive'
  ELSE 'cheap' END AS cheap_or_expensive
FROM Facilities

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */

SELECT firstname, surname, joindate
FROM Members
WHERE joindate = (SELECT MAX(joindate) FROM Members)

-- JOIN more than two tables (time measurement)
/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

-- WHERE, no duplicate: GROUP BY
-- Performance 1st. Showing rows 0 - 29 (46 total, Query took 0.0002 sec)
SELECT Facilities.name, CONCAT(Members.firstname, ' ', Members.surname) AS member_name
FROM Bookings
INNER JOIN Members ON Bookings.memid = Members.memid
INNER JOIN Facilities ON Bookings.facid = Facilities.facid
WHERE Facilities.name LIKE 'Tennis Court%'
GROUP BY Facilities.name, Members.firstname, Members.surname
ORDER BY Members.firstname


-- using subquery, WHERE, no duplicate: GROUP BY
-- Performance 2nd. Showing rows 0 - 29 (46 total, Query took 0.0077 sec)
/*
SELECT sub.facname, CONCAT(sub.firstname, ' ', sub.surname) AS member_name
FROM (
  SELECT Facilities.name AS facname, Members.firstname AS firstname, Members.surname AS surname
  FROM Bookings
  INNER JOIN Members ON Bookings.memid = Members.memid
  INNER JOIN Facilities ON Bookings.facid = Facilities.facid
  WHERE Facilities.name LIKE 'Tennis Court%'
) sub
GROUP BY sub.facname, sub.firstname, sub.surname
ORDER BY sub.firstname
*/


-- JOIN ON "AND", no duplicate: GROUP BY
-- Performance 3rd. Showing rows 0 - 29 (46 total, Query took 0.0084 sec)
/*
SELECT Facilities.name, CONCAT(Members.firstname, ' ', Members.surname) AS member_name
FROM Bookings
INNER JOIN Members ON Bookings.memid = Members.memid
INNER JOIN Facilities ON Bookings.facid = Facilities.facid
AND Facilities.name LIKE 'Tennis Court%'
GROUP BY Facilities.name, Members.firstname, Members.surname
ORDER BY Members.firstname
*/


-- no duplicate: DISTINCT, WHERE
-- Performance 4th. Showing rows 0 - 29 (46 total, Query took 0.0155 sec)
/*
SELECT DISTINCT Facilities.name, CONCAT(Members.firstname, ' ', Members.surname) AS member_name
FROM Bookings
INNER JOIN Members ON Bookings.memid = Members.memid
INNER JOIN Facilities ON Bookings.facid = Facilities.facid
WHERE Facilities.name LIKE 'Tennis Court%'
ORDER BY Members.firstname
*/


/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

--Showing rows 0 - 11 (12 total, Query took 0.0023 sec)
SELECT Facilities.name,
  CONCAT(Members.firstname, ' ', Members.surname) AS member_name,
  CASE WHEN Members.memid !=0
    THEN Bookings.slots * Facilities.membercost
    ELSE Bookings.slots * Facilities.guestcost
    END AS booking_cost
FROM Bookings
INNER JOIN Members ON Bookings.memid = Members.memid
INNER JOIN Facilities ON Bookings.facid = Facilities.facid
WHERE Bookings.starttime LIKE '2012-09-14%'
  AND(
    (Bookings.memid != 0 AND Bookings.slots * Facilities.membercost > 30)
    OR (Bookings.memid = 0 AND Bookings.slots * Facilities.guestcost > 30)
  )
ORDER BY booking_cost DESC

--WHERE (filter after join) --> AND (filter before join)
/*
SELECT Facilities.name,
  CONCAT(Members.firstname, ' ', Members.surname) AS member_name,
  CASE WHEN Members.memid !=0
    THEN Bookings.slots * Facilities.membercost
    ELSE Bookings.slots * Facilities.guestcost
    END AS booking_cost
FROM Bookings
INNER JOIN Members ON Bookings.memid = Members.memid
INNER JOIN Facilities ON Bookings.facid = Facilities.facid
AND Bookings.starttime LIKE '2012-09-14%'
  AND(
    (Bookings.memid != 0 AND Bookings.slots * Facilities.membercost > 30)
    OR (Bookings.memid = 0 AND Bookings.slots * Facilities.guestcost > 30)
  )
ORDER BY booking_cost DESC
*/


/* Q9: This time, produce the same result as in Q8, but using a subquery. */

--Showing rows 0 - 11 (12 total, Query took 0.0023 sec) [booking_cost: 320.0 - 35.0]
SELECT *
FROM (
  SELECT Facilities.name,
  CONCAT(Members.firstname, ' ', Members.surname) AS member_name,
  CASE WHEN Members.memid !=0
    THEN Bookings.slots * Facilities.membercost
    ELSE Bookings.slots * Facilities.guestcost
    END AS booking_cost
  FROM Bookings
  INNER JOIN Members ON Bookings.memid = Members.memid
  INNER JOIN Facilities ON Bookings.facid = Facilities.facid
  WHERE Bookings.starttime LIKE '2012-09-14%'
  ) sub
WHERE sub.booking_cost > 30
ORDER BY sub.booking_cost DESC

/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

--Showing rows 0 - 2 (3 total, Query took 0.0109 sec)
--[note] AS facility_total_revenue: Retrieved table should have table name
SELECT facility, total_revenue
FROM (
  SELECT Facilities.name AS facility,
  SUM(
    CASE WHEN Bookings.memid !=0
    THEN Bookings.slots * Facilities.membercost
    ELSE Bookings.slots * Facilities.guestcost END) AS total_revenue
  FROM Facilities
  INNER JOIN Bookings ON Bookings.facid = Facilities.facid
  GROUP BY Facilities.name
) AS facility_total_revenue
WHERE total_revenue < 1000
ORDER BY total_revenue

--nested subqueries
--howing rows 0 - 2 (3 total, Query took 0.0103 sec) [total_revenue: 180.0 - 270.0]
/*
SELECT *
FROM (
  SELECT sub_cost.facility, SUM(sub_cost.revenue) AS total_revenue
    FROM (
      SELECT Facilities.name AS facility,
          CASE WHEN Bookings.memid !=0
          THEN Bookings.slots * Facilities.membercost
          ELSE Bookings.slots * Facilities.guestcost
          END AS revenue
      FROM Facilities
      INNER JOIN Bookings ON Bookings.facid = Facilities.facid
    ) sub_cost
  GROUP BY sub_cost.facility
) sub_sum
WHERE sub_sum.total_revenue < 1000
ORDER BY sub_sum.total_revenue
*/
