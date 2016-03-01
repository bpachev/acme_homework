from bs4 import BeautifulSoup
import re

#Problem 1
# Part 1
print "Problem 1 (i) Tags used: html, head, title, meta, style, body, div, h1, p, a"

# Part 2
print "Problem 1 (ii) style:type = 'text/css'"

#Problem 2
html_doc = """
<html><head><title>The Three Stooges</title></head>
<body>
<p class="title"><b>The Three Stooges</b></p>
<p class="story">Have you ever met the three stooges? Their names are
<a href="http://example.com/larry" class="stooge" id="link1">Larry</a>,
<a href="http://example.com/mo" class="stooge" id="link2">Mo</a> and
<a href="http://example.com/curly" class="stooge" id="link3">Curly</a>;
and they are really hilarious.</p>
<p class="story">...</p>   """

print "\nProblem 2, prettified soup"
soup = BeautifulSoup(html_doc,'html.parser')
print soup.prettify()
#Problem 3
print "\nProblem 3"
print "soup.p returns a tag object representing the <p> tag, the first such tag"
print "string representation: <p> tag: " + str(soup.p)

#Problem 4
# Part 1
print "\nProblem 4 (i)"
bod = soup.body
p2 = bod.p.next_sibling.next_sibling
print p2.a.next_sibling.next_sibling.contents

# Part 2
print "\nProblem 4 (ii)"
print p2

# Part 3
print "\nProblem 4 (iii), first method (note) 4(iii) is the same as 5"
soup = BeautifulSoup(open('example.htm'))
print soup.body.div.p.next_sibling.next_sibling.a['href']
#Pass

#Problem 5
soup = BeautifulSoup(open('example.htm'))
print "\nProblem 5, second method"
print soup.find('a')['href']

#Problem 6
# Part 1
print "\nProblem 6 (i)"
SOUP = BeautifulSoup(open('SanDiegoWeather2.htm'))
print SOUP.find(text="Thursday, January 1, 2015").parent

# Part 2
print "\nProblem 6 (ii)"
print "Previous Day: " + SOUP.find("div",attrs={"class":"previous-link"}).a['href']
print "Next Day: " + SOUP.find("div",attrs={"class":"next-link"}).a['href']

# Part 3
print "\nProblem 6 (iii)"
print "Actual Max Temperature: " + SOUP.find(text="Max Temperature").parent.parent.next_sibling.next_sibling.span.span.text + "F"

#Problem 7
dates_soup = BeautifulSoup(open('Big-Data-dates1.htm'))
print dates_soup.find(href=re.compile("d+"))
#Pass
