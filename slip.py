#!/usr/bin/env python
# -*- coding: utf8 -*-
from fpdf import FPDF, HTMLMixin
import csv, os, sys
from datetime import date, datetime

def generateHTML(r):
    html = """
    <b>PRONTO GROUP LTD.</b>           TAX ID: 0105551086096<br/>
    15 Rajanakarn Building 3rd, 6th and 7th Floor, Soi Pradipat 17, <br/>
    Pradipat Road, Samsennai, Phayathai, Bangkok
    <table border=1 width="100%%">
    <thead><tr>
    <th width="35%%">Period:  %s</th><th width="35%%">Start Date:  %s</th><th width="30%%">ID:  %s</th>
    </tr></thead>
    <tbody>
    <tr>
    <td width="50%%">Name:    %s</td><td width="50%%">Tax ID:    %s</td>
    </tr>
    <tr>
    <td width="50%%">Position:    %s</td><td width="50%%">Department:    %s</td>
    </tr>
    <tr bgcolor="#03aced"><th width="50%%">Income</th><th width="50%%">Deduction</th></tr>
    <tr>
    <td width="25%%" border="1">Salary</td><td width="25%%" align="right">%s</td><td width="25%%">Tax</td><td width="25%%" align="right">%s</td>
    </tr>
    <tr>
    <td width="25%%">Daily</td><td width="25%%" align="right">-</td><td width="25%%">Social Security</td><td width="25%%" align="right">%s</td>
    </tr>
    <tr>
    <td width="25%%">Bonus</td><td width="25%%" align="right">%s</td><td width="25%%">Advance</td><td width="25%%" align="right">-</td>
    </tr>
    <tr>
    <td width="25%%">Others</td><td width="25%%" align="right">-</td><td width="25%%">Fund Load/Other deduct</td><td width="25%%" align="right">%s</td>
    </tr>
    <tr>
    <td width="25%%" >Commission</td><td width="25%%" align="right">%s</td><td width="25%%">Provident Fund</td><td width="25%%" align="right">%s</td>
    </tr>
    <tr>
    <td width="25%%">OT/Shifters/Others</td><td width="25%%" align="right">%s</td><td width="25%%">Remark</td><td width="25%%" align="right">-</td>
    </tr>
    <tr>
    <td width="25%%">Kbank Acc No.</td><td width="25%%" align="right">%s</td><td width="25%%">  </td><td width="25%%">    </td>
    </tr>
    <tr>
    <th width="25%%">Gross Earning</th><th width="25%%" align="right">%s</th><th width="25%%">Total deduction</th><th width="25%%" align="right">%s</th>
    </tr>
    <tr>
    <th width="50%%">                    </th><th width="25%%">Net Pay</th><th width="25%%" align="right">%s</th>
    </tr>
    <tr bgcolor="#03aced">
    <th width="25%%">Acc. Income</th><th width="25%%">Acc. Tax</th><th width="25%%">Acc. Provident Fund</th><th width="25%%">Acc. Social Security</th>
    </tr>
    <tr>
    <th width="25%%">%s</th><th width="25%%">%s</th><th width="25%%">%s</th><th width="25%%">%s</th>
    </tr>
    <tr>
    <td width="100%%"><i>This letter is computer-generated no signature is required</i></td>
    </tr>
    </tbody>
    </table></br>""" % ( 
        r['period'],r['start_date'], r['employee_id'], r['name'], 
        r['employee_tax_id'], r['position'], r['department'], r['salary'], 
        r['tax'], r['social_security'],r['bonus'],r['other_deduct'],
        r['commissions'],r['provident_fund'],r['shifter'],r['bank_ac'],
        r['net_income'],r['net_deduct'],r['net_paid'],
        r['ytd_net_income'],r['ytd_tax'],r['ytd_provident_fund'],r['ytd_sso'])
    return html


def write_HTML(record):
    pdf=MyFPDF()
    #First page
    pdf.add_page()
    pdf.set_font('Arial', '', 5)
    html = generateHTML(record)
    pdf.image('pronto-logo-header.png', x = 150, y = 10, w = 50)
    pdf.write_html(html)
    path = "exported/"
    if not os.path.exists(path):
        os.makedirs(path)
    pdf.output(path+record['employee_id']+"_"+record['name']+"_"+record['period']+".pdf", 'F')

def readAll(file):
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None) #skip header
        records = list(reader)
    for record in records:
        extracted = csv_extract(record)
        write_HTML(extracted)

def csv_extract(record):
    period=datetime.strptime(record[0].strip(), '%m/%d/%y')
    start_date=datetime.strptime(record[5].strip(), '%m/%d/%y')
    employee_id=record[1]
    name=record[2]
    employee_tax_id=record[7]
    position=record[4]
    department=record[3]
    salary=record[25]
    tax=record[29]
    social_security=record[30]
    bonus=record[28]
    other_deduct=record[31]
    commissions=record[27]
    provident_fund=record[32]
    shifter=record[26]
    bank_ac=record[6]
    net_income=record[34]
    net_paid=record[33]
    net_deduct=record[35]
    ytd_net_income=record[23]
    ytd_tax=record[18]
    ytd_provident_fund=record[21]
    ytd_sso=record[19]

    return {
        'period': datetime.strftime(period, '%d %B %Y'),
        'start_date': datetime.strftime(start_date, '%d %B %Y'),
        'employee_id': employee_id.strip(),
        'name': name.strip(),
        'employee_tax_id': employee_tax_id.strip(),
        'position': position.strip(),
        'department': department.strip(),
        'salary': salary.strip(),
        'tax': tax.strip(),
        'social_security': social_security.strip(),
        'bonus': bonus.strip(),
        'other_deduct': other_deduct.strip(),
        'commissions': commissions.strip(),
        'provident_fund': provident_fund.strip(),
        'shifter': shifter.strip(),
        'bank_ac': bank_ac.strip(),
        'net_income': net_income.strip(),
        'net_deduct': net_deduct.strip(),
        'net_paid': net_paid.strip(),
        'ytd_net_income': ytd_net_income.strip(),
        'ytd_tax': ytd_tax.strip(),
        'ytd_provident_fund': ytd_provident_fund.strip(),
        'ytd_sso': ytd_sso.strip()}

class MyFPDF(FPDF, HTMLMixin):
    pass

if __name__ == "__main__":
    readAll(str(sys.argv[1]))
 