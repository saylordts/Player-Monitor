from _3_Write_Report.writeHTML import writeHTML
from _DClasses.report import Report
from _3_Write_Report.writeMJML import writeMJML

def writeReport(report: Report):
   mjml = writeMJML(report)
   html = writeHTML(mjml)
   report.html = html
   return report
