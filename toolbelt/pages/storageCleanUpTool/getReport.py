def getReport(reportPath, dataArray, toolInfo): 
    with open(reportPath, "w") as html:
        #html head
        html.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>storage clean up report</title>\n</head>\n')
    
        #html body (where the info will be placed)
        html.write('<body>\n')
        html.write('<main>\n')
        html.write('<h1>Storage Clean Up Report</h1><br>\n')
        html.write(f"<h3>I've Checked {toolInfo[1]} files in {toolInfo[0]} seconds</h3>")
        for type in dataArray: # 3 types
            html.write(f'<h2>{type} ({len(dataArray[type])})</h2>\n')
            for file in dataArray[type]:
                print(file)
                html.write('<fileColum>\n')
                html.write('<fileSize>%s</fileSize>\n' % file[1])
                html.write('<filePath>%s</filePath>\n' % file[0])
                html.write('</fileColum>\n')
            
        
        html.write('</main>\n')
        html.write('</body>\n')
        html.write('<style>\n* {transition: 50ms;}\nh1 {color: blue; text-align: center;}\nh3 {text-align: center;}\n body {display: flex; justify-content: center; margin: 0;}\nmain {display: block; width: 80vw; border-left: 1px solid grey; border-right: 1px solid grey; padding: 10px;}\nfileColum {display: flex;}\nfileSize {width: 150px; color: red;}\n filePath:hover {color: rgb(0,175,0)}\n</style>\n')
        html.write('</html>')
        html.close()
