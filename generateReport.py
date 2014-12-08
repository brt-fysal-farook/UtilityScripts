#!/usr/bin/python

import pprint
import re
import subprocess
import sys

try:
    from openpyxl.workbook import Workbook
    from openpyxl.styles import Alignment, Border, Color, Font, PatternFill, Side, Style
    from openpyxl.cell import Cell
except ImportError:
    print('You need to execute:\n\tsudo pip install openpyxl')
    sys.exit(-1)

codeReviewSearchURL = """https://codereview.chromium.org/search?closed=1&owner=%s&reviewer=&cc=&repo_guid=&base=&project=&private=1&commit=1&created_before=&created_after=&modified_before=&modified_after=&order=&format=html&keys_only=False&with_messages=False&cursor=&limit=30"""
codeReviewURL = 'https://codereview.chromium.org/user/'
repositories = [
    {
        'name': 'blink',
        'path': '/home/vivekg/workspace/report-generation/blink',
        'type': 'git'
    },
    {
        'name': 'chromium',
        'path': '/home/vivekg/workspace/report-generation/chromium',
        'type': 'git'
    },
    {
        'name': 'skia',
        'path': '/home/vivekg/workspace/report-generation/skia',
        'type': 'git'
    },
    {
        'name': 'trace-viewer',
        'path': '/home/vivekg/workspace/report-generation/trace-viewer',
        'type': 'git'
    },
    {
        'name': 'v8',
        'path': '/home/vivekg/workspace/report-generation/v8',
        'type': 'git'
    }
]

authors = [
    { 'name': 'Abhijeet Kandalkar', 'email': 'xxx@yyy.com' },
    { 'name': 'Ajay Berwal', 'email': 'xxx@yyy.com' },
    { 'name': 'Akhil Teeka Dhananjaya', 'email': 'xxx@yyy.com' },
    { 'name': 'Behara Mani Shyam Patro', 'email': 'xxx@yyy.com' },
    { 'name': 'Gandhi Kishor Addanki', 'email': 'xxx@yyy.com' },
    { 'name': 'Ganesh Kamat', 'email': 'xxx@yyy.com' },
    { 'name': 'Kaja Mohaideen', 'email': 'xxx@yyy.com' },
    { 'name': 'Karthik Gopalan', 'email': 'xxx@yyy.com' },
    { 'name': 'Kulajit Das', 'email': 'xxx@yyy.com' },
    { 'name': 'Mallikarjuna Narala', 'email': 'xxx@yyy.com' },
    { 'name': 'Munukutla Subrahmanya Praveen', 'email': 'xxx@yyy.com' },
    { 'name': 'Nikhil Sahni', 'email': 'xxx@yyy.com' },
    { 'name': 'Pavan Kumar Emani', 'email': 'xxx@yyy.com' },
    { 'name': 'Prabhavathi Perumal', 'email': 'xxx@yyy.com' },
    { 'name': 'Prashant Nevase', 'email': 'xxx@yyy.com' },
    { 'name': 'Putturaju R', 'email': 'xxx@yyy.com' },
    { 'name': 'Ravi Kasibhatla', 'email': 'xxx@yyy.com' },
    { 'name': 'Shanmuga Pandi', 'email': 'xxx@yyy.com' },
    { 'name': 'Siva Gunturi', 'email': 'xxx@yyy.com' },
    { 'name': 'Sohan Jyoti Ghosh', 'email': 'xxx@yyy.com' },
    { 'name': 'Suchit Agarwal', 'email': 'xxx@yyy.com' },
    { 'name': 'Sujith S S', 'email': 'xxx@yyy.com' },
    { 'name': 'Suyash Sengar', 'email': 'xxx@yyy.com' },
    { 'name': 'Tanvir Rizvi', 'email': 'xxx@yyy.com' },
    { 'name': 'Thanikassalam Kankayan', 'email': 'xxx@yyy.com' },
    { 'name': 'Vivek Agrawal', 'email': 'xxx@yyy.com' },
    { 'name': 'Vivek Galatage', 'email': ['xxx@yyy.com', 'xxx@yyy.com', 'xxx@yyy.com', 'xxx@yyy.com'] }
]

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'))

greyTheme = Style(
    border=thin_border,
    fill=PatternFill(fill_type='solid', start_color='FFD8D8D8'))

whiteTheme = Style(
    border=thin_border,
    fill=PatternFill(fill_type='solid', start_color='FFFFFFFF'))

def beautifyWorksheet(sheet):
    sheet.column_dimensions['A'].width = 30
    sheet.row_dimensions[1].height = 30
    sheet.row_dimensions[sheet.get_highest_row()].height = 30

    for col in ['B', 'C', 'D', 'E', 'F', 'G']:
        sheet.column_dimensions[col].width = 12

    header = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1']
    lastRow = str(sheet.get_highest_row())
    footer = ['A' + lastRow, 'B' + lastRow, 'C' + lastRow, 'D' + lastRow, 'E' + lastRow, 'F' + lastRow, 'G' + lastRow]

    for col in header:
        sheet[col].style = Style(
            alignment=Alignment(vertical='bottom', horizontal='center'),
            border=thin_border,
            fill=PatternFill(fill_type='solid', start_color='FFFFFF99'),
            font=Font(bold=True))

    for col in footer:
        sheet[col].style = Style(
            border=thin_border,
            fill=PatternFill(fill_type='solid', start_color='FFFFFF99'),
            font=Font(bold=True))

    for col in range(sheet.get_highest_column()):
        for row in range(1, sheet.get_highest_row() - 1):
            cell = sheet[str(chr(col + 65) + str(row + 1))]
            if (row % 2) == 0:
                cell.style = greyTheme
            else:
                cell.style = whiteTheme

def generateReport():
    wb = Workbook()
    totals = wb.create_sheet(index=0, title='Total')
    totals['A1'] = 'Name'
    totals['B1'] = 'Chromium'
    totals['C1'] = 'Blink'
    totals['D1'] = 'Trace-Viewer'
    totals['E1'] = 'Skia'
    totals['F1'] = 'V8'
    totals['G1'] = 'Total'

    for i in range(len(authors)):
        author = authors[i]
        index = str(i + 2)
        totals['A' + index] = author['name']

        if type(author['email']) == list:
            totals['A' + index].hyperlink = codeReviewSearchURL % author['email'][0]
        else:
            totals['A' + index].hyperlink = codeReviewSearchURL % author['email']

        if 'contributions' not in author:
            continue;

        contributions = author['contributions']

        repoToColumnTuples = [
            ('B', 'chromium'),
            ('C', 'blink'),
            ('D', 'trace-viewer'),
            ('E', 'skia'),
            ('F', 'v8'),
        ]

        for (col, repo) in repoToColumnTuples:
            if repo in contributions:
                totals[col + index] = contributions[repo]['total']

        totals['G' + index] = '=sum(b%s:f%s)' % (index, index)
    finalRowIndex = str(len(authors) + 2)
    dataRange = '(%s2:%s' + str(len(authors) + 1) + ')'
    totals['A' + finalRowIndex] = 'Total'

    for col in ['B', 'C', 'D', 'E', 'F', 'G']:
        totals[col + finalRowIndex] = '=sum' + (dataRange % (col, col))
    beautifyWorksheet(totals)
    wb.save('weeklyReport.xlsx')

def execute(cwd, command, verbose=True, progress=False):
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    processOutput = []
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        processOutput.append(nextline)
        if (verbose):
            sys.stdout.write(nextline)
            sys.stdout.flush()
        if (progress):
            sys.stdout.write('.')
            sys.stdout.flush()
    if (progress):
        print('')
    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return processOutput
    else:
        raise ProcessException(command, exitCode, output)

def getAllAuthorEmails():
    authorEmails = []
    for author in authors:
        if (type(author['email']) == list):
            authorEmails = authorEmails +  author['email']
        elif (type(author['email']) == str):
            authorEmails.append(author['email'])
    return authorEmails

def populateContributions():
    print('Calculating the contributions made so far...')
    authorEmails = getAllAuthorEmails()
    authorsList = []
    for email in authorEmails:
        authorsList.append('\(' + email + '\)')
    authorsString = '\|'.join(authorsList)

    for repo in repositories:
        output = execute(repo['path'], 'git shortlog -es --author=\'' + authorsString +'\'', False)
        allContributions = {}
        for line in output:
            details = line.split()
            commits = int(details[0])
            retriedEmail = details[len(details) - 1]
            email = re.compile('((^<)(\w+\.?\w+@\w+.?\w+)(.*$))').match(retriedEmail).groups()[2]
            if email not in allContributions:
                allContributions[email] = commits
            else:
                allContributions[email] = allContributions[email] + commits
        if not len(allContributions):
            continue

        for i in range(len(authors)):
            emailType = type(authors[i]['email'])
            commits = 0
            if emailType == list:
                for eachEmail in authors[i]['email']:
                    if eachEmail in allContributions:
                        commits = commits + allContributions[eachEmail]
            elif emailType == str:
                email = authors[i]['email']
                if email in allContributions:
                    commits = allContributions[email]
            if commits:
                repoName = repo['name']
                if 'contributions' not in authors[i]:
                    authors[i]['contributions'] = {}
                if repoName not in authors[i]['contributions']:
                    authors[i]['contributions'][repoName] = {}
                authors[i]['contributions'][repoName]['total'] = commits

def updateRepositories():
    for repo in repositories:
        sys.stdout.write('Updating repository: ' + repo['name'])
        if (repo['type'] == 'git'):
            output = execute(repo['path'], 'git pull', False, True)

def main():
    #updateRepositories()
    populateContributions()
    #pprint.pprint(authors, width=1)
    generateReport()

if __name__ == '__main__':
    sys.exit(main())
