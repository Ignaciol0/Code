from PIL import Image, ImageDraw
import aspose.words as aw
import os
import cv2
import cvzone
from VideoMaker import create_vid

player = "Maradona"
Hook = f'Have you watched {player}?'
path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/"
info = ["100","193","31","fr","Real Madrid",False,['RW','CM']]
matches = [['Barcelona',3,5,'10'],['Manchester United',3,3,'9.57']]
stats = [9.05,'Matches Played: 24(14)','Goals: 11','Assist: 4','Big Chances: 7','Progresive Passes: 39','Dribbles %: 61.6% ']
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def make_ig_story(path,player, Hook):
    # I used the Anonymous Pro font since is a fixed font and this seems to be the formula:
    # to get the witdh which is the characters in the line times the weight and the whole divided by two
    font_size1 = 45
    font_size2 = 40
    size1 = ((len(Hook)*font_size1)/2)-len(Hook)
    size2 = (((len(player)+13)*font_size2)/2)-len(player)-13
    # then to find the displacement we substract the size to the total width and divide the number by 2
    svg_code =f"""<svg width="750" height="1334" viewBox="0 0 750 1334" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image height="1334" x="-300" preserveAspectRatio="none" href="./images/background.png"></image>
    <text fill="white" font-family="Anonymous Pro" font-size="{font_size1}" font-weight="bold"  x="{(750 -size1)//2}" y="170">{Hook}</text>
    <text fill="white" font-family="Anonymous Pro" font-size="{font_size2}" font-weight="bold"  x="{(750 -size2)//2}" y="720">See {player} analysis</text>
    <path d="M357 614.75L361.229 610.725L371.583 620.931V586H377.417V620.931L387.771 610.725L392 614.75L374.5 632L357 614.75Z" fill="white"/>
    </svg>"""


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/background.png')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    post1 = cv2.imread(path+'Ig post 1.png')

    #Background adjusting
    height, witdh, channels = background.shape
    scale = height / 1334
    witdh = int(witdh / scale)
    background = cv2.resize(background,(witdh,1334))
    offset = abs((witdh-1080)//2)
    background = background[0:1334,offset:offset+750]
    #Overlay adjusting
    height, witdh, channels = overlay.shape
    offset_x = int((750-witdh)/2)
    imgResult = cvzone.overlayPNG(background,overlay,[offset_x,0])
    cv2.imwrite(path+'ig.png', imgResult)

    #Post adjusting
    height, width, channels = post1.shape
    scale = width / 460
    height = int(height / scale)
    post1 = cv2.resize(post1,(460, 497))
    cv2.imwrite(path+"Ig post 1.png", post1)


    background = Image.open(path+"ig.png")
    post1 = Image.open(path+"Ig post 1.png").convert("RGBA")
    background.paste(post1, (145,649), mask= post1)
    background.save(path+"Ig storie.png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")
    os.remove(path+'ig.png')

def make_ig_post1(path, youngster=False):
    if youngster:
        position_x = 240
        text = "Youngster"
    else:
        position_x = 290
        text = "Player"
    # then to find the displacement we substract the size to the total width and divide the number by 2
    svg_code =f"""<svg width="1088" height="1132" viewBox="0 0 1088 1132" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect y="980" width="1088" height="152" fill="url(#paint0_linear_289_12)"/>
    <rect x="1084" y="152" width="1088" height="152" transform="rotate(-180 1084 152)" fill="url(#paint1_linear_289_12)"/>
    <text fill="white" font-family="Inter" font-weight="bold" font-size="50" x="{position_x}" y="100" text-decoration='underline'>{text} Scout Analysis</text>
    <text x='400' y="1047" font-size="50" fill="white" font-family="Inter" font-weight="bold">Who is he?</text>
    <path d="M684.19 1047.72L680.071 1043.63L690.884 1032.82H665.547V1026.82H690.884L680.071 1016.02L684.19 1011.92L702.088 1029.82L684.19 1047.72Z" fill="white"/>
    <defs>
    <linearGradient id="paint0_linear_289_12" x1="544" y1="972" x2="544" y2="1124" gradientUnits="userSpaceOnUse">
    <stop stop-color="#1C1C1C" stop-opacity="0.23"/>
    <stop offset="1" stop-color="#1C1C1C"/>
    </linearGradient>
    <linearGradient id="paint1_linear_289_12" x1="1624" y1="152" x2="1624" y2="304" gradientUnits="userSpaceOnUse">
    <stop stop-color="#1C1C1C" stop-opacity="0.23"/>
    <stop offset="1" stop-color="#1C1C1C"/>
    </linearGradient>
    </defs>
    </svg>
    """


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/photo1.jpg')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)

    #Background adjusting
    height, width, channels = background.shape
    if height - (0.1* height) > width:
        scale = width / 1080
        height = int(height / scale)
        background = cv2.resize(background,(1080,height))
    else:
        scale = height / 1124
        width = int(width / scale)
        background = cv2.resize(background,(width,1124))
    offset = abs((width-1080)//2)
    background = background[0:1124,offset:offset+1080]

    #Overlay adjusting
    height, witdh, channels = overlay.shape
    overlay = cv2.resize(overlay,(1080,1124))
    imgResult = cvzone.overlayPNG(background,overlay,[0,0])
    cv2.imwrite(path+'Ig post 1.png', imgResult)

    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_ig_post2(path,player,info):
    """Path: is the path to the directory all the images are in
       Player: is the name of the player analyzed 
       Info: is a list of [value, height, age , nation, club, right footed = bool]"""
    
    positions = info[6]
    positions_text = ''
    for e in positions:
        if 'L' in e:
            y = 76
            if 'W' in e:
                x = 385
            elif 'B' in e:
                x = 104
            else:
                x = 296
        elif 'R' in e:
            y = 264
            if 'W' in e:
                x = 385
            elif 'B' in e:
                x = 104
            else:
                x = 296
        else:
            y = 170
            if 'D' in e:
                x = 191
            elif 'B' in e:
                x = 104
            elif 'C' in e:
                x = 285
            elif 'A' in e:
                x = 380
            else:
                x = 474
        if 'WB' in e:
            if "RWB" == e:
                positions_text += f'''<rect x="188" y="264" width="100" height="46" rx="23" fill="#24E513"/>
                                    <text x='205' y='298' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
                                '''
            if "LWB" == e:
                positions_text += f'''<rect x="188" y="76" width="100" height="46" rx="23" fill="#24E513"/>
                                    <text x='205' y='110' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
                                '''
        else:
            positions_text += f'''<rect x="{x}" y="{y}" width="80" height="46" rx="23" fill="#24E513"/>
                                    <text x='{x+16}' y='{y + 34}' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
    '''
    position_svg = f'''
        <g clip-path="url(#clip0_984_26)" transform='translate(566,650) scale(0.8)'>
        <rect width="568" height="386" rx="40" fill="#005B3A"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M282 234.953V385.5H286V234.953C308.267 233.909 326 215.525 326 193C326 170.475 308.267 152.091 286 151.047V-1.5H282V151.047C259.733 152.091 242 170.475 242 193C242 215.525 259.733 233.909 282 234.953ZM286 230.948C306.057 229.908 322 213.316 322 193C322 172.684 306.057 156.092 286 155.052V230.948ZM282 155.052V230.948C261.943 229.908 246 213.316 246 193C246 172.684 261.943 156.092 282 155.052ZM487 80.5C487 79.3954 487.895 78.5 489 78.5H569V82.5H491V297H569V301H489C487.895 301 487 300.105 487 299V229.233C475.426 220.075 468 205.905 468 190C468 174.095 475.426 159.925 487 150.767V80.5ZM487 156.014C477.783 164.426 472 176.538 472 190C472 203.462 477.783 215.574 487 223.986V156.014ZM533 143C533 141.895 533.895 141 535 141H569V145H537V234H569V238H535C533.895 238 533 237.105 533 236V143ZM80 300.5C81.1046 300.5 82 299.605 82 298.5V228.233C93.574 219.075 101 204.905 101 189C101 173.095 93.574 158.925 82 149.767V80C82 78.8954 81.1046 78 80 78H0V82H78V296.5H0V300.5H80ZM97 189C97 202.462 91.2171 214.573 82 222.986V155.014C91.2171 163.426 97 175.538 97 189ZM34 238C35.1046 238 36 237.105 36 236V143C36 141.895 35.1046 141 34 141H0V145H32V234H0V238H34Z" fill="white"/>
        {positions_text}
        </g>
    '''
    
    if info[5]:
        left_color = '#636363'
        right_color = 'white'
    else:
        left_color = 'white'
        right_color = '#636363'
    # then to find the displacement we substract the size to the total width and divide the number by 2
    svg_code =f"""<svg width="1088" height="1132" viewBox="0 0 1088 1132" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g filter="url(#filter0_d_533_22)">
                <rect y="980" width="1088" height="152" fill="url(#paint0_linear_533_22)"/>
                <text fill="white" font-family="Inter" font-weight="bold" font-size="50" x="280" y="1050">Key stats analysis -></text>
                <rect width="489" height="404" rx="40" transform="matrix(-1 0 0 1 544 557)" fill="#1D1D1D"/>
                <path d="M91 651.307H511" stroke="#525252" stroke-linecap="round"/>
                <path d="M329.465 845.26C328.53 845.251 327.528 845.609 326.506 846.363C325.018 847.46 323.607 849.401 322.813 851.893C322.018 854.386 322.017 856.873 322.556 858.754C323.094 860.636 324.071 861.831 325.331 862.319C326.591 862.807 328.033 862.549 329.521 861.452C331.008 860.356 332.418 858.414 333.213 855.922C334.007 853.429 334.009 850.942 333.471 849.061C332.932 847.179 331.954 845.984 330.695 845.496C330.299 845.343 329.884 845.263 329.465 845.26ZM340.058 852.923C339.489 852.926 338.874 853.102 338.223 853.471C338.099 854.86 337.823 856.228 337.401 857.544C336.653 859.892 335.512 861.938 334.099 863.56C334.113 863.628 334.127 863.696 334.142 863.762C334.507 865.324 335.23 866.291 336.174 866.722C337.119 867.153 338.245 867.031 339.494 866.205C340.742 865.379 341.987 863.837 342.742 861.796C343.498 859.756 343.591 857.688 343.226 856.126C342.862 854.564 342.139 853.598 341.195 853.167C340.835 853.002 340.448 852.92 340.058 852.923ZM349.135 860.85C348.736 860.853 348.298 860.929 347.822 861.091C347.732 861.122 347.64 861.163 347.548 861.199C347.376 862.043 347.141 862.869 346.845 863.669C345.873 866.293 344.345 868.442 342.492 869.898C342.616 870.994 343.019 871.775 343.62 872.266C344.343 872.857 345.338 873.026 346.61 872.595C347.881 872.164 349.308 871.087 350.399 869.441C351.491 867.794 351.992 865.963 351.984 864.488C351.975 863.013 351.534 862.01 350.81 861.42C350.358 861.051 349.801 860.847 349.135 860.85ZM320.14 863.999C318.076 865.947 316.798 868.687 316.062 873.742C314.55 884.13 317.316 894.374 316.429 909.344C316.145 914.138 314.291 919.219 312.328 924.234C310.364 929.248 308.254 934.189 307.271 938.078C306.659 940.499 307.121 942.232 308.282 943.823C309.443 945.414 311.455 946.741 313.83 947.407C318.582 948.738 324.354 947.438 327.304 942.535C336.592 927.097 348.349 905.83 351.841 894.299C351.996 893.787 352.048 893.154 352 892.428C351.881 892.331 351.763 892.229 351.649 892.12C350.097 890.628 349.502 888.358 349.641 886.233C349.655 886.019 349.677 885.806 349.704 885.594C349.642 885.477 349.582 885.362 349.516 885.245C349.507 885.228 349.496 885.21 349.487 885.193C348.749 885.01 348.033 884.682 347.376 884.179C345.555 882.787 344.664 880.446 344.575 878.126C344.441 877.961 344.301 877.798 344.165 877.634C343.043 877.452 341.958 877 341 876.218C339.632 875.102 338.761 873.512 338.334 871.773C337.057 871.963 335.744 871.823 334.496 871.253C332.54 870.36 331.135 868.596 330.33 866.522C328.298 867.511 326.018 867.773 323.859 866.937C322.354 866.354 321.107 865.312 320.14 863.999ZM354.67 871.178C354.453 871.582 354.218 871.974 353.967 872.354C352.621 874.384 350.914 875.912 349.052 876.817C348.992 877.208 348.965 877.583 348.976 877.925C349.015 879.063 349.358 879.739 349.848 880.114C350.338 880.489 351.025 880.6 351.984 880.225C352.942 879.85 354.045 878.947 354.87 877.59C355.696 876.233 356.042 874.752 356.004 873.614C355.965 872.476 355.622 871.8 355.132 871.425C354.99 871.317 354.835 871.234 354.67 871.178ZM358.513 881.392C358.334 881.398 358.132 881.428 357.905 881.488C357.845 881.504 357.782 881.528 357.72 881.548C356.855 882.676 355.85 883.584 354.76 884.238C354.307 885.066 354.068 885.916 354.023 886.61C353.963 887.54 354.18 888.059 354.496 888.363C354.813 888.667 355.302 888.828 356.108 888.614C356.914 888.4 357.912 887.757 358.717 886.695C359.522 885.633 359.929 884.422 359.99 883.492C360.05 882.562 359.833 882.044 359.517 881.739C359.319 881.549 359.054 881.415 358.686 881.394C358.628 881.39 358.571 881.39 358.513 881.392Z" fill="{right_color}"/>
                <path d="M268.535 845.26C269.47 845.251 270.472 845.609 271.494 846.363C272.982 847.46 274.393 849.401 275.187 851.893C275.982 854.386 275.983 856.873 275.444 858.754C274.906 860.636 273.929 861.831 272.669 862.319C271.409 862.807 269.967 862.549 268.479 861.452C266.992 860.356 265.582 858.414 264.787 855.922C263.993 853.429 263.991 850.942 264.529 849.061C265.068 847.179 266.046 845.984 267.305 845.496C267.701 845.343 268.116 845.263 268.535 845.26ZM257.942 852.923C258.511 852.926 259.126 853.102 259.777 853.471C259.901 854.86 260.177 856.228 260.599 857.544C261.347 859.892 262.488 861.938 263.901 863.56C263.887 863.628 263.873 863.696 263.858 863.762C263.493 865.324 262.77 866.291 261.826 866.722C260.881 867.153 259.755 867.031 258.506 866.205C257.258 865.379 256.013 863.837 255.258 861.796C254.502 859.756 254.409 857.688 254.774 856.126C255.138 854.564 255.861 853.598 256.805 853.167C257.165 853.002 257.552 852.92 257.942 852.923ZM248.865 860.85C249.264 860.853 249.702 860.929 250.178 861.091C250.268 861.122 250.36 861.163 250.452 861.199C250.624 862.043 250.859 862.869 251.155 863.669C252.127 866.293 253.655 868.442 255.508 869.898C255.384 870.994 254.981 871.775 254.38 872.266C253.657 872.857 252.662 873.026 251.39 872.595C250.119 872.164 248.692 871.087 247.601 869.441C246.509 867.794 246.008 865.963 246.016 864.488C246.025 863.013 246.466 862.01 247.19 861.42C247.642 861.051 248.199 860.847 248.865 860.85ZM277.86 863.999C279.924 865.947 281.202 868.687 281.938 873.742C283.45 884.13 280.684 894.374 281.571 909.344C281.855 914.138 283.709 919.219 285.672 924.234C287.636 929.248 289.746 934.189 290.729 938.078C291.341 940.499 290.879 942.232 289.718 943.823C288.557 945.414 286.545 946.741 284.17 947.407C279.418 948.738 273.646 947.438 270.696 942.535C261.408 927.097 249.651 905.83 246.159 894.299C246.004 893.787 245.952 893.154 246 892.428C246.119 892.331 246.237 892.229 246.351 892.12C247.903 890.628 248.498 888.358 248.359 886.233C248.345 886.019 248.323 885.806 248.296 885.594C248.358 885.477 248.418 885.362 248.484 885.245C248.493 885.228 248.504 885.21 248.513 885.193C249.251 885.01 249.967 884.682 250.624 884.179C252.445 882.787 253.336 880.446 253.425 878.126C253.559 877.961 253.699 877.798 253.835 877.634C254.957 877.452 256.042 877 257 876.218C258.368 875.102 259.239 873.512 259.666 871.773C260.943 871.963 262.256 871.823 263.504 871.253C265.46 870.36 266.865 868.596 267.67 866.522C269.702 867.511 271.982 867.773 274.141 866.937C275.646 866.354 276.893 865.312 277.86 863.999ZM243.33 871.178C243.547 871.582 243.782 871.974 244.033 872.354C245.379 874.384 247.086 875.912 248.948 876.817C249.008 877.208 249.035 877.583 249.024 877.925C248.985 879.063 248.642 879.739 248.152 880.114C247.662 880.489 246.975 880.6 246.016 880.225C245.058 879.85 243.955 878.947 243.13 877.59C242.304 876.233 241.958 874.752 241.996 873.614C242.035 872.476 242.378 871.8 242.868 871.425C243.01 871.317 243.165 871.234 243.33 871.178ZM239.487 881.392C239.666 881.398 239.868 881.428 240.095 881.488C240.155 881.504 240.218 881.528 240.28 881.548C241.145 882.676 242.15 883.584 243.24 884.238C243.693 885.066 243.932 885.916 243.977 886.61C244.037 887.54 243.82 888.059 243.504 888.363C243.187 888.667 242.698 888.828 241.892 888.614C241.086 888.4 240.088 887.757 239.283 886.695C238.478 885.633 238.071 884.422 238.01 883.492C237.95 882.562 238.167 882.044 238.483 881.739C238.681 881.549 238.946 881.415 239.314 881.394C239.372 881.39 239.429 881.39 239.487 881.392Z" fill="{left_color}"/>
                </g>
                <text x='225' y="745" font-size="24" fill="white" font-family="Inter" font-weight="bold">Value: {info[0]}M</text>
                <text x='100' y="795" font-size="24" fill="white" font-family="Inter" font-weight="bold">Age: {info[2]} yrs</text>
                <text x='325' y="795" font-size="24" fill="white" font-family="Inter" font-weight="bold">Height: {info[1]} cm</text>
                <text x='{(489-(((len(player))*30)/2)-len(player))//2+50}' y="630" font-size="30" fill="white" font-family="Inter" font-weight="bold">{player}</text>
                <text x='265' y="825" font-size="24" fill="white" font-family="Inter" font-weight="bold">Foot:</text>
                <text x='100' y="695" font-size="24" fill="white" font-family="Inter" font-weight="bold">Nation:</text>
                <text x='325' y="695" font-size="24" fill="white" font-family="Inter" font-weight="bold">Club:</text>
                
                {position_svg}
                <defs>
                <linearGradient id="paint0_linear_533_22" x1="544" y1="972" x2="544" y2="1124" gradientUnits="userSpaceOnUse">
                <stop stop-color="#1C1C1C" stop-opacity="0.23"/>
                <stop offset="1" stop-color="#1C1C1C"/>
                </linearGradient>
                </defs>
                </svg>
                """


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/photo2.jpg')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    img_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Resources/'
    nation = Image.open(img_path+f'Nations/{info[3]}.webp').convert("RGBA")
    club = Image.open(img_path+f'Clubs/{info[4]}.webp').convert("RGBA")

    #Background adjusting
    height, width, channels = background.shape
    if height - (0.1* height) > width:
        scale = width / 1080
        height = int(height / scale)
        background = cv2.resize(background,(1080,height))
    else:
        scale = height / 1124
        width = int(width / scale)
        background = cv2.resize(background,(width,1124))
    offset = abs((width-1080)//2)
    background = background[0:1124,offset:offset+1080]

    #Overlay adjusting
    height, witdh, channels = overlay.shape
    overlay = cv2.resize(overlay,(1080,1124))
    imgResult = cvzone.overlayPNG(background,overlay,[0,0])
    cv2.imwrite(path+'Ig post 2(no club nation).png', imgResult)

    # Club adjusting
    height, width = club.size
    scale = height / 45
    width = int(width / scale)
    club = club.resize((45,width))

    # Nation adjusting
    nation = nation.resize((45,45))

    imgResult = Image.open(path+'Ig post 2(no club nation).png')
    imgResult.paste(nation, (212,660), mask= nation)
    imgResult.paste(club, (402,(663-(width-45))), mask= club)
    imgResult.save(path+"Ig post 2.png")

    
    os.remove(path+"Ig post 2(no club nation).png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_ig_post3(path,matches,stats):
    """Path: is the path to the directory all the images are in
       matches: is a list with the match stats. [[club name,goals,assists,rating],[club name,goals,assists,rating]]
       stats: is a list with the season stats. [rating,matches_played,goals (g/a in case of a defender),assists (good stat 1 in case a defender),good stat 1, good stat 2, good stat 3, good stat 4, good stat 5]
    """
    # We are getting the stats of the square by duplicating the texts that appear and making the y increase
    year_rating = stats[0]
    stats = stats[1:]
    stats_text = ''
    for stat in stats:
        stats_text += f'<text fill="white" font-family="Inter" font-size="26" font-weight="bold" x="305" y="{520+stats.index(stat)*30}">{stat}</text>\n'
    percentile_height = 520+(len(stats))*30
    # Now we are making the match part of the post
        # We start calculating the separation needed between the rating and the badges
    gamatch1 = matches[0][1]+matches[0][2]
    gamatch2 = matches[1][1]+matches[1][2]
    match_separation_half = ((max(gamatch1,gamatch2) * 59)//2)+50
    gamatch1_text = ''
    g1,a1 = matches[0][1], matches[0][2]
    gamatch2_text = ''
    g2,a2 = matches[1][1], matches[1][2]
    
    # Now we calculate the first match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    inital_x_g = (544 - ((gamatch1*59)//2)) - 472
    inital_x_a = (544 - ((gamatch1*59)//2)) + 59*g1
    if g1 > 0:
        for g in range(g1):
            gamatch1_text += f'<path transform="translate({inital_x_g+59*g},0)" d="M500.5 290C496.419 290 492.584 289.225 488.995 287.675C485.406 286.128 482.284 284.026 479.629 281.371C476.974 278.716 474.872 275.594 473.325 272.005C471.775 268.416 471 264.581 471 260.5C471 256.419 471.775 252.584 473.325 248.995C474.872 245.406 476.974 242.284 479.629 239.629C482.284 236.974 485.406 234.871 488.995 233.322C492.584 231.774 496.419 231 500.5 231C504.581 231 508.416 231.774 512.005 233.322C515.594 234.871 518.716 236.974 521.371 239.629C524.026 242.284 526.128 245.406 527.675 248.995C529.225 252.584 530 256.419 530 260.5C530 264.581 529.225 268.416 527.675 272.005C526.128 275.594 524.026 278.716 521.371 281.371C518.716 284.026 515.594 286.128 512.005 287.675C508.416 289.225 504.581 290 500.5 290ZM515.25 253.125L519.233 251.798L520.413 247.815C518.839 245.455 516.946 243.426 514.734 241.729C512.521 240.034 510.088 238.768 507.433 237.932L503.45 240.735V244.865L515.25 253.125ZM485.75 253.125L497.55 244.865V240.735L493.567 237.932C490.912 238.768 488.479 240.034 486.266 241.729C484.054 243.426 482.161 245.455 480.588 247.815L481.768 251.798L485.75 253.125ZM482.652 275.84L486.045 275.545L488.257 271.562L483.98 258.73L479.85 257.255L476.9 259.467C476.9 262.663 477.342 265.576 478.227 268.205C479.112 270.837 480.587 273.382 482.652 275.84ZM500.5 284.1C501.778 284.1 503.032 284.002 504.261 283.805C505.49 283.608 506.695 283.313 507.875 282.92L509.94 278.495L508.023 275.25H492.977L491.06 278.495L493.125 282.92C494.305 283.313 495.51 283.608 496.739 283.805C497.968 284.002 499.222 284.1 500.5 284.1ZM493.863 269.35H507.138L511.267 257.55L500.5 250.028L489.88 257.55L493.863 269.35ZM518.347 275.84C520.412 273.382 521.888 270.837 522.772 268.205C523.657 265.576 524.1 262.663 524.1 259.467L521.15 257.403L517.02 258.73L512.743 271.562L514.955 275.545L518.347 275.84Z" fill="#0FB916"/>\n'
    if a1 > 0:
        for a in range(a1):
            gamatch1_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+59*a},240)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    
    
    # Now we calculate the second match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    inital_x_g = (544 -((gamatch2*59)//2)) - 472
    inital_x_a = (544 -((gamatch2*59)//2)) + 59*g2
    if g2 > 0:
        for g in range(g2):
            gamatch2_text += f'<path transform="translate({inital_x_g+59*g},80)" d="M500.5 290C496.419 290 492.584 289.225 488.995 287.675C485.406 286.128 482.284 284.026 479.629 281.371C476.974 278.716 474.872 275.594 473.325 272.005C471.775 268.416 471 264.581 471 260.5C471 256.419 471.775 252.584 473.325 248.995C474.872 245.406 476.974 242.284 479.629 239.629C482.284 236.974 485.406 234.871 488.995 233.322C492.584 231.774 496.419 231 500.5 231C504.581 231 508.416 231.774 512.005 233.322C515.594 234.871 518.716 236.974 521.371 239.629C524.026 242.284 526.128 245.406 527.675 248.995C529.225 252.584 530 256.419 530 260.5C530 264.581 529.225 268.416 527.675 272.005C526.128 275.594 524.026 278.716 521.371 281.371C518.716 284.026 515.594 286.128 512.005 287.675C508.416 289.225 504.581 290 500.5 290ZM515.25 253.125L519.233 251.798L520.413 247.815C518.839 245.455 516.946 243.426 514.734 241.729C512.521 240.034 510.088 238.768 507.433 237.932L503.45 240.735V244.865L515.25 253.125ZM485.75 253.125L497.55 244.865V240.735L493.567 237.932C490.912 238.768 488.479 240.034 486.266 241.729C484.054 243.426 482.161 245.455 480.588 247.815L481.768 251.798L485.75 253.125ZM482.652 275.84L486.045 275.545L488.257 271.562L483.98 258.73L479.85 257.255L476.9 259.467C476.9 262.663 477.342 265.576 478.227 268.205C479.112 270.837 480.587 273.382 482.652 275.84ZM500.5 284.1C501.778 284.1 503.032 284.002 504.261 283.805C505.49 283.608 506.695 283.313 507.875 282.92L509.94 278.495L508.023 275.25H492.977L491.06 278.495L493.125 282.92C494.305 283.313 495.51 283.608 496.739 283.805C497.968 284.002 499.222 284.1 500.5 284.1ZM493.863 269.35H507.138L511.267 257.55L500.5 250.028L489.88 257.55L493.863 269.35ZM518.347 275.84C520.412 273.382 521.888 270.837 522.772 268.205C523.657 265.576 524.1 262.663 524.1 259.467L521.15 257.403L517.02 258.73L512.743 271.562L514.955 275.545L518.347 275.84Z" fill="#0FB916"/>\n'
    if a2 > 0:
        for a in range(a2):
            gamatch2_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+59*a},320)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    

    # THIS IS THE SVG CODE

    svg_code =f"""<svg width="1088" height="1132" viewBox="0 0 1088 1132" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <text fill="white" font-family="Inter" font-size="35" font-weight="bold" x="250" y="65">Season 2022/2023 Achievements</text>

                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="35" x="345" y="135">Average Seasson Rating</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="50" x="480" y="200">{year_rating}</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="35" x="600" y="200">rtg</text>

                    <rect x="{544-match_separation_half - 95}" y="220" width="95" height="79" fill="none"/>
                    {gamatch1_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="60" x="{544+match_separation_half}" y="280">{matches[0][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="30" x="{544+match_separation_half+140}" y="280">rtg</text>

                    <rect x="{544-match_separation_half - 95}" y="300" width="95" height="79" fill="none"/>
                    {gamatch2_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="60" x="{544+match_separation_half}" y="360">{matches[1][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="30" x="{544+match_separation_half+140}" y="360">rtg</text>

                    <rect x="300" y="698.065" width="494" height="309.494" rx="15" fill="white"/>

                    <rect width="560" height="633" rx="40" transform="matrix(-1 0 0 1 824 408)" fill="#1D1D1D"/>
                    <text fill="white" font-family="Inter" font-size="30" font-weight="bold" x="420" y="460">This season stats</text>
                    <path d="M306.373 480.18H787.355" stroke="#525252" stroke-linecap="round"/>

                    {stats_text}
                </svg>"""


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/background.png')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    img_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Resources/'
    club1 = Image.open(img_path+f'Clubs/{matches[0][0]}.webp').convert("RGBA")
    club2 = Image.open(img_path+f'Clubs/{matches[1][0]}.webp').convert("RGBA")
    percentiles = Image.open(path+f'images/percentiles.png')

    #Background adjusting
    background = background[100:1224,250:1330]

    #Overlay adjusting
    height, witdh, channels = overlay.shape
    overlay = cv2.resize(overlay,(1080,1124))
    imgResult = cvzone.overlayPNG(background,overlay,[0,0])
    cv2.imwrite(path+'Ig post 3(no clubs).png', imgResult)

    # Percentiles
    width, height = percentiles.size
    multiplier = width / 470
    height = int(height / multiplier)
    percentiles = percentiles.resize((470,height))
    percentile_offset = 544 - 470 // 2 
    percentiles = add_corners(percentiles,20)

    # Club adjusting
    club_size = 70

    width, height = club1.size
    scale = width / club_size
    height1 = int(height / scale)
    club1 = club1.resize((club_size,height1))
    width,height = club2.size
    scale = width / club_size
    height2 = int(height / scale)
    club2 = club2.resize((club_size,height2))

    imgResult = Image.open(path+'Ig post 3(no clubs).png')
    imgResult.paste(club1, (544-match_separation_half - club_size,(220-(height1-club_size)//2)), mask= club1)
    imgResult.paste(club2, (544-match_separation_half - club_size,(300-(height2-club_size)//2)), mask= club2)
    imgResult.paste(percentiles, (percentile_offset,percentile_height ), mask= percentiles)
    imgResult.save(path+"Ig post 3.png")

    
    os.remove(path+"Ig post 3(no clubs).png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_video1(path, player):
    from PIL import ImageFont
    true = True
    font_size = 95
    while true:
        font = ImageFont.truetype('C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/font/Inter-3.19/Inter Desktop/Inter-Bold.otf', font_size)
        width = font.getlength(f'{player}')
        if width < 700:
            break
        else:
            font_size -= 5
    with open(path+'svg.svg','w') as f:
        f.write(f"""
                <svg width="1088" height="1920" viewBox="0 0 1088 1920">
                <text x='{544-width//2}' y="645" font-size="{font_size}" fill="white"  stroke="black"  font-family="Inter" font-weight="bold">{player}</text>
                </svg>
                """)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    background = cv2.imread(path+'images/photo1.jpg')
    height, width, channels = background.shape
    scale = height / 1920
    width = int(width / scale)
    background = cv2.resize(background,(width,1920))
    height, width, channels = background.shape
    width = (width - 1080)//2
    background = background[0:1920,width:1080+width]
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    overlay = cv2.resize(overlay,(1088,1920))
    cvzone.overlayPNG(background,overlay,[0,0])
    cv2.imwrite(path+"Video.png", background)    
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_video2(path,player,info):
    """Path: is the path to the directory all the images are in
       Player: is the name of the player analyzed 
       Info: is a list of [value, height, age , nation, club, right footed = bool]"""
    
    positions = info[6]
    positions_text = ''
    for e in positions:
        if 'L' in e:
            y = 76
            if 'W' in e:
                x = 385
            elif 'B' in e:
                x = 104
            else:
                x = 296
        elif 'R' in e:
            y = 264
            if 'W' in e:
                x = 385
            elif 'B' in e:
                x = 104
            else:
                x = 296
        else:
            y = 170
            if 'D' in e:
                x = 191
            elif 'B' in e:
                x = 104
            elif 'C' in e:
                x = 285
            elif 'A' in e:
                x = 380
            else:
                x = 474
        if 'WB' in e:
            if "RWB" == e:
                positions_text += f'''<rect x="188" y="264" width="100" height="46" rx="23" fill="#24E513"/>
                                    <text x='205' y='298' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
                                '''
            if "LWB" == e:
                positions_text += f'''<rect x="188" y="76" width="100" height="46" rx="23" fill="#24E513"/>
                                    <text x='205' y='110' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
                                '''
        else:
            positions_text += f'''<rect x="{x}" y="{y}" width="80" height="46" rx="23" fill="#24E513"/>
                                    <text x='{x+16}' y='{y + 34}' fill="white" font-family="Inter" font-weight="bold" font-size="30">{e}</text>
    '''
    position_svg = f'''
        <g clip-path="url(#clip0_984_26)" transform='translate(420,1521)'>
        <rect width="568" height="386" rx="40" fill="#005B3A"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M282 234.953V385.5H286V234.953C308.267 233.909 326 215.525 326 193C326 170.475 308.267 152.091 286 151.047V-1.5H282V151.047C259.733 152.091 242 170.475 242 193C242 215.525 259.733 233.909 282 234.953ZM286 230.948C306.057 229.908 322 213.316 322 193C322 172.684 306.057 156.092 286 155.052V230.948ZM282 155.052V230.948C261.943 229.908 246 213.316 246 193C246 172.684 261.943 156.092 282 155.052ZM487 80.5C487 79.3954 487.895 78.5 489 78.5H569V82.5H491V297H569V301H489C487.895 301 487 300.105 487 299V229.233C475.426 220.075 468 205.905 468 190C468 174.095 475.426 159.925 487 150.767V80.5ZM487 156.014C477.783 164.426 472 176.538 472 190C472 203.462 477.783 215.574 487 223.986V156.014ZM533 143C533 141.895 533.895 141 535 141H569V145H537V234H569V238H535C533.895 238 533 237.105 533 236V143ZM80 300.5C81.1046 300.5 82 299.605 82 298.5V228.233C93.574 219.075 101 204.905 101 189C101 173.095 93.574 158.925 82 149.767V80C82 78.8954 81.1046 78 80 78H0V82H78V296.5H0V300.5H80ZM97 189C97 202.462 91.2171 214.573 82 222.986V155.014C91.2171 163.426 97 175.538 97 189ZM34 238C35.1046 238 36 237.105 36 236V143C36 141.895 35.1046 141 34 141H0V145H32V234H0V238H34Z" fill="white"/>
        {positions_text}
        </g>
    '''
    if info[5]:
        left_color = '#636363'
        right_color = 'white'
    else:
        left_color = 'white'
        right_color = '#636363'
    
    from PIL import ImageFont
    font = ImageFont.truetype('C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/font/Inter-3.19/Inter Desktop/Inter-Bold.otf', 35)
    width = font.getlength(f'{player}')
    # then to find the displacement we substract the size to the total width and divide the number by 2
    svg_code =f"""
                <svg width="1088" height="1920" viewBox="0 0 1088 1920" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g transform='translate(0,-70)'>
                <rect width="620" height="512" rx="40" transform="matrix(-1 0 0 1 1044 1057)" fill="#1D1D1D"/>
                <path transform='translate(320,500)' d="M131 651.307H711" stroke="#525252" stroke-linecap="round"/>
                <path transform='translate(440,560)' d="M329.465 845.26C328.53 845.251 327.528 845.609 326.506 846.363C325.018 847.46 323.607 849.401 322.813 851.893C322.018 854.386 322.017 856.873 322.556 858.754C323.094 860.636 324.071 861.831 325.331 862.319C326.591 862.807 328.033 862.549 329.521 861.452C331.008 860.356 332.418 858.414 333.213 855.922C334.007 853.429 334.009 850.942 333.471 849.061C332.932 847.179 331.954 845.984 330.695 845.496C330.299 845.343 329.884 845.263 329.465 845.26ZM340.058 852.923C339.489 852.926 338.874 853.102 338.223 853.471C338.099 854.86 337.823 856.228 337.401 857.544C336.653 859.892 335.512 861.938 334.099 863.56C334.113 863.628 334.127 863.696 334.142 863.762C334.507 865.324 335.23 866.291 336.174 866.722C337.119 867.153 338.245 867.031 339.494 866.205C340.742 865.379 341.987 863.837 342.742 861.796C343.498 859.756 343.591 857.688 343.226 856.126C342.862 854.564 342.139 853.598 341.195 853.167C340.835 853.002 340.448 852.92 340.058 852.923ZM349.135 860.85C348.736 860.853 348.298 860.929 347.822 861.091C347.732 861.122 347.64 861.163 347.548 861.199C347.376 862.043 347.141 862.869 346.845 863.669C345.873 866.293 344.345 868.442 342.492 869.898C342.616 870.994 343.019 871.775 343.62 872.266C344.343 872.857 345.338 873.026 346.61 872.595C347.881 872.164 349.308 871.087 350.399 869.441C351.491 867.794 351.992 865.963 351.984 864.488C351.975 863.013 351.534 862.01 350.81 861.42C350.358 861.051 349.801 860.847 349.135 860.85ZM320.14 863.999C318.076 865.947 316.798 868.687 316.062 873.742C314.55 884.13 317.316 894.374 316.429 909.344C316.145 914.138 314.291 919.219 312.328 924.234C310.364 929.248 308.254 934.189 307.271 938.078C306.659 940.499 307.121 942.232 308.282 943.823C309.443 945.414 311.455 946.741 313.83 947.407C318.582 948.738 324.354 947.438 327.304 942.535C336.592 927.097 348.349 905.83 351.841 894.299C351.996 893.787 352.048 893.154 352 892.428C351.881 892.331 351.763 892.229 351.649 892.12C350.097 890.628 349.502 888.358 349.641 886.233C349.655 886.019 349.677 885.806 349.704 885.594C349.642 885.477 349.582 885.362 349.516 885.245C349.507 885.228 349.496 885.21 349.487 885.193C348.749 885.01 348.033 884.682 347.376 884.179C345.555 882.787 344.664 880.446 344.575 878.126C344.441 877.961 344.301 877.798 344.165 877.634C343.043 877.452 341.958 877 341 876.218C339.632 875.102 338.761 873.512 338.334 871.773C337.057 871.963 335.744 871.823 334.496 871.253C332.54 870.36 331.135 868.596 330.33 866.522C328.298 867.511 326.018 867.773 323.859 866.937C322.354 866.354 321.107 865.312 320.14 863.999ZM354.67 871.178C354.453 871.582 354.218 871.974 353.967 872.354C352.621 874.384 350.914 875.912 349.052 876.817C348.992 877.208 348.965 877.583 348.976 877.925C349.015 879.063 349.358 879.739 349.848 880.114C350.338 880.489 351.025 880.6 351.984 880.225C352.942 879.85 354.045 878.947 354.87 877.59C355.696 876.233 356.042 874.752 356.004 873.614C355.965 872.476 355.622 871.8 355.132 871.425C354.99 871.317 354.835 871.234 354.67 871.178ZM358.513 881.392C358.334 881.398 358.132 881.428 357.905 881.488C357.845 881.504 357.782 881.528 357.72 881.548C356.855 882.676 355.85 883.584 354.76 884.238C354.307 885.066 354.068 885.916 354.023 886.61C353.963 887.54 354.18 888.059 354.496 888.363C354.813 888.667 355.302 888.828 356.108 888.614C356.914 888.4 357.912 887.757 358.717 886.695C359.522 885.633 359.929 884.422 359.99 883.492C360.05 882.562 359.833 882.044 359.517 881.739C359.319 881.549 359.054 881.415 358.686 881.394C358.628 881.39 358.571 881.39 358.513 881.392Z" fill="{right_color}"/>
                <path transform='translate(440,560)' d="M268.535 845.26C269.47 845.251 270.472 845.609 271.494 846.363C272.982 847.46 274.393 849.401 275.187 851.893C275.982 854.386 275.983 856.873 275.444 858.754C274.906 860.636 273.929 861.831 272.669 862.319C271.409 862.807 269.967 862.549 268.479 861.452C266.992 860.356 265.582 858.414 264.787 855.922C263.993 853.429 263.991 850.942 264.529 849.061C265.068 847.179 266.046 845.984 267.305 845.496C267.701 845.343 268.116 845.263 268.535 845.26ZM257.942 852.923C258.511 852.926 259.126 853.102 259.777 853.471C259.901 854.86 260.177 856.228 260.599 857.544C261.347 859.892 262.488 861.938 263.901 863.56C263.887 863.628 263.873 863.696 263.858 863.762C263.493 865.324 262.77 866.291 261.826 866.722C260.881 867.153 259.755 867.031 258.506 866.205C257.258 865.379 256.013 863.837 255.258 861.796C254.502 859.756 254.409 857.688 254.774 856.126C255.138 854.564 255.861 853.598 256.805 853.167C257.165 853.002 257.552 852.92 257.942 852.923ZM248.865 860.85C249.264 860.853 249.702 860.929 250.178 861.091C250.268 861.122 250.36 861.163 250.452 861.199C250.624 862.043 250.859 862.869 251.155 863.669C252.127 866.293 253.655 868.442 255.508 869.898C255.384 870.994 254.981 871.775 254.38 872.266C253.657 872.857 252.662 873.026 251.39 872.595C250.119 872.164 248.692 871.087 247.601 869.441C246.509 867.794 246.008 865.963 246.016 864.488C246.025 863.013 246.466 862.01 247.19 861.42C247.642 861.051 248.199 860.847 248.865 860.85ZM277.86 863.999C279.924 865.947 281.202 868.687 281.938 873.742C283.45 884.13 280.684 894.374 281.571 909.344C281.855 914.138 283.709 919.219 285.672 924.234C287.636 929.248 289.746 934.189 290.729 938.078C291.341 940.499 290.879 942.232 289.718 943.823C288.557 945.414 286.545 946.741 284.17 947.407C279.418 948.738 273.646 947.438 270.696 942.535C261.408 927.097 249.651 905.83 246.159 894.299C246.004 893.787 245.952 893.154 246 892.428C246.119 892.331 246.237 892.229 246.351 892.12C247.903 890.628 248.498 888.358 248.359 886.233C248.345 886.019 248.323 885.806 248.296 885.594C248.358 885.477 248.418 885.362 248.484 885.245C248.493 885.228 248.504 885.21 248.513 885.193C249.251 885.01 249.967 884.682 250.624 884.179C252.445 882.787 253.336 880.446 253.425 878.126C253.559 877.961 253.699 877.798 253.835 877.634C254.957 877.452 256.042 877 257 876.218C258.368 875.102 259.239 873.512 259.666 871.773C260.943 871.963 262.256 871.823 263.504 871.253C265.46 870.36 266.865 868.596 267.67 866.522C269.702 867.511 271.982 867.773 274.141 866.937C275.646 866.354 276.893 865.312 277.86 863.999ZM243.33 871.178C243.547 871.582 243.782 871.974 244.033 872.354C245.379 874.384 247.086 875.912 248.948 876.817C249.008 877.208 249.035 877.583 249.024 877.925C248.985 879.063 248.642 879.739 248.152 880.114C247.662 880.489 246.975 880.6 246.016 880.225C245.058 879.85 243.955 878.947 243.13 877.59C242.304 876.233 241.958 874.752 241.996 873.614C242.035 872.476 242.378 871.8 242.868 871.425C243.01 871.317 243.165 871.234 243.33 871.178ZM239.487 881.392C239.666 881.398 239.868 881.428 240.095 881.488C240.155 881.504 240.218 881.528 240.28 881.548C241.145 882.676 242.15 883.584 243.24 884.238C243.693 885.066 243.932 885.916 243.977 886.61C244.037 887.54 243.82 888.059 243.504 888.363C243.187 888.667 242.698 888.828 241.892 888.614C241.086 888.4 240.088 887.757 239.283 886.695C238.478 885.633 238.071 884.422 238.01 883.492C237.95 882.562 238.167 882.044 238.483 881.739C238.681 881.549 238.946 881.415 239.314 881.394C239.372 881.39 239.429 881.39 239.487 881.392Z" fill="{left_color}"/>
                <text x='650' y="1265" font-size="30" fill="white" font-family="Inter" font-weight="bold">Value: {info[0]}M</text>
                <text x='525' y="1325" font-size="30" fill="white" font-family="Inter" font-weight="bold">Age: {info[2]} yrs</text>
                <text x='775' y="1325" font-size="30" fill="white" font-family="Inter" font-weight="bold">Height: {info[1]} cm</text>
                <text x='{424+(620-width)//2}' y="1130" font-size="35" fill="white" font-family="Inter" font-weight="bold">{player}</text>
                <text x='700' y="1380" font-size="30" fill="white" font-family="Inter" font-weight="bold">Foot:</text>
                <text x='525' y="1210" font-size="30" fill="white" font-family="Inter" font-weight="bold">Nation:</text>
                <text x='775' y="1210" font-size="30" fill="white" font-family="Inter" font-weight="bold">Club:</text>
                </g>
                {position_svg}
                </svg>
                """


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/photo2.jpg')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    img_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Resources/'
    nation = Image.open(img_path+f'Nations/{info[3]}.webp').convert("RGBA")
    club = Image.open(img_path+f'Clubs/{info[4]}.webp').convert("RGBA")

    #Background adjusting
    height, width, channels = background.shape
    if height - (0.6* height) > width:
        scale = width / 1080
        height = int(height / scale)
        background = cv2.resize(background,(1080,height))
    else:
        scale = height / 1920
        width = int(width / scale)
        background = cv2.resize(background,(width,1920))
    offset = abs((width-1080)//2)
    background = background[0:1920,offset:offset+1080]

    #Overlay adjusting
    height, witdh, channels = overlay.shape
    overlay = cv2.resize(overlay,(1080,1920))
    imgResult = cvzone.overlayPNG(background,overlay,[0,-100])
    cv2.imwrite(path+'Video2(no clubs).png', imgResult)

    # Club adjusting
    width,height = club.size
    scale = width / 45
    height = int(height / scale)
    club = club.resize((45,height))
    # Nation adjusting
    nation = nation.resize((45,45))

    imgResult = Image.open(path+'video2(no clubs).png')
    imgResult.paste(nation, (655,997), mask= nation)
    imgResult.paste(club, (870,997), mask= club)
    imgResult.save(path+"Video-1.png")

    
    os.remove(path+"Video2(no clubs).png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_video3(path,matches,stats):
    """Path: is the path to the directory all the images are in
       matches: is a list with the match stats. [[club name,goals,assists,rating],[club name,goals,assists,rating]]
       stats: is a list with the season stats. [rating,matches_played,goals (g/a in case of a defender),assists (good stat 1 in case a defender),good stat 1, good stat 2, good stat 3, good stat 4, good stat 5]
    """
    # We are getting the stats of the square by duplicating the texts that appear and making the y increase
    year_rating = stats[0]
    stats = stats[1:]
    stats_text = ''
    for stat in stats:
        stats_text += f'<text fill="white" font-family="Inter" font-size="35" font-weight="bold" x="320" y="{520+stats.index(stat)*40}">{stat}</text>\n'
    percentile_height = 520+(len(stats))*30
    # Now we are making the match part of the post
        # We start calculating the separation needed between the rating and the badges
    gamatch1 = matches[0][1]+matches[0][2]
    gamatch2 = matches[1][1]+matches[1][2]
    match_separation_half = ((max(gamatch1,gamatch2) * 59)//2)+50
    gamatch1_text = ''
    g1,a1 = matches[0][1], matches[0][2]
    gamatch2_text = ''
    g2,a2 = matches[1][1], matches[1][2]
    
    # Now we calculate the first match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    inital_x_g = (544 - ((gamatch1*59)//2)) - 472
    inital_x_a = (544 - ((gamatch1*59)//2)) + 59*g1
    if g1 > 0:
        for g in range(g1):
            gamatch1_text += f'<path transform="translate({inital_x_g+59*g},0)" d="M500.5 290C496.419 290 492.584 289.225 488.995 287.675C485.406 286.128 482.284 284.026 479.629 281.371C476.974 278.716 474.872 275.594 473.325 272.005C471.775 268.416 471 264.581 471 260.5C471 256.419 471.775 252.584 473.325 248.995C474.872 245.406 476.974 242.284 479.629 239.629C482.284 236.974 485.406 234.871 488.995 233.322C492.584 231.774 496.419 231 500.5 231C504.581 231 508.416 231.774 512.005 233.322C515.594 234.871 518.716 236.974 521.371 239.629C524.026 242.284 526.128 245.406 527.675 248.995C529.225 252.584 530 256.419 530 260.5C530 264.581 529.225 268.416 527.675 272.005C526.128 275.594 524.026 278.716 521.371 281.371C518.716 284.026 515.594 286.128 512.005 287.675C508.416 289.225 504.581 290 500.5 290ZM515.25 253.125L519.233 251.798L520.413 247.815C518.839 245.455 516.946 243.426 514.734 241.729C512.521 240.034 510.088 238.768 507.433 237.932L503.45 240.735V244.865L515.25 253.125ZM485.75 253.125L497.55 244.865V240.735L493.567 237.932C490.912 238.768 488.479 240.034 486.266 241.729C484.054 243.426 482.161 245.455 480.588 247.815L481.768 251.798L485.75 253.125ZM482.652 275.84L486.045 275.545L488.257 271.562L483.98 258.73L479.85 257.255L476.9 259.467C476.9 262.663 477.342 265.576 478.227 268.205C479.112 270.837 480.587 273.382 482.652 275.84ZM500.5 284.1C501.778 284.1 503.032 284.002 504.261 283.805C505.49 283.608 506.695 283.313 507.875 282.92L509.94 278.495L508.023 275.25H492.977L491.06 278.495L493.125 282.92C494.305 283.313 495.51 283.608 496.739 283.805C497.968 284.002 499.222 284.1 500.5 284.1ZM493.863 269.35H507.138L511.267 257.55L500.5 250.028L489.88 257.55L493.863 269.35ZM518.347 275.84C520.412 273.382 521.888 270.837 522.772 268.205C523.657 265.576 524.1 262.663 524.1 259.467L521.15 257.403L517.02 258.73L512.743 271.562L514.955 275.545L518.347 275.84Z" fill="#0FB916"/>\n'
    if a1 > 0:
        for a in range(a1):
            gamatch1_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+59*a},240)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    
    
    # Now we calculate the second match goals and assists
            
    # First we calculate the initial points knowing that the desired point is the half of the width 544 minus half of the ga's width
            # In the one of the goal we substract 472 due to this being the displacement of the path
            # In the one of the assist we add the length of the goals
    inital_x_g = (544 -((gamatch2*59)//2)) - 472
    inital_x_a = (544 -((gamatch2*59)//2)) + 59*g2
    if g2 > 0:
        for g in range(g2):
            gamatch2_text += f'<path transform="translate({inital_x_g+59*g},80)" d="M500.5 290C496.419 290 492.584 289.225 488.995 287.675C485.406 286.128 482.284 284.026 479.629 281.371C476.974 278.716 474.872 275.594 473.325 272.005C471.775 268.416 471 264.581 471 260.5C471 256.419 471.775 252.584 473.325 248.995C474.872 245.406 476.974 242.284 479.629 239.629C482.284 236.974 485.406 234.871 488.995 233.322C492.584 231.774 496.419 231 500.5 231C504.581 231 508.416 231.774 512.005 233.322C515.594 234.871 518.716 236.974 521.371 239.629C524.026 242.284 526.128 245.406 527.675 248.995C529.225 252.584 530 256.419 530 260.5C530 264.581 529.225 268.416 527.675 272.005C526.128 275.594 524.026 278.716 521.371 281.371C518.716 284.026 515.594 286.128 512.005 287.675C508.416 289.225 504.581 290 500.5 290ZM515.25 253.125L519.233 251.798L520.413 247.815C518.839 245.455 516.946 243.426 514.734 241.729C512.521 240.034 510.088 238.768 507.433 237.932L503.45 240.735V244.865L515.25 253.125ZM485.75 253.125L497.55 244.865V240.735L493.567 237.932C490.912 238.768 488.479 240.034 486.266 241.729C484.054 243.426 482.161 245.455 480.588 247.815L481.768 251.798L485.75 253.125ZM482.652 275.84L486.045 275.545L488.257 271.562L483.98 258.73L479.85 257.255L476.9 259.467C476.9 262.663 477.342 265.576 478.227 268.205C479.112 270.837 480.587 273.382 482.652 275.84ZM500.5 284.1C501.778 284.1 503.032 284.002 504.261 283.805C505.49 283.608 506.695 283.313 507.875 282.92L509.94 278.495L508.023 275.25H492.977L491.06 278.495L493.125 282.92C494.305 283.313 495.51 283.608 496.739 283.805C497.968 284.002 499.222 284.1 500.5 284.1ZM493.863 269.35H507.138L511.267 257.55L500.5 250.028L489.88 257.55L493.863 269.35ZM518.347 275.84C520.412 273.382 521.888 270.837 522.772 268.205C523.657 265.576 524.1 262.663 524.1 259.467L521.15 257.403L517.02 258.73L512.743 271.562L514.955 275.545L518.347 275.84Z" fill="#0FB916"/>\n'
    if a2 > 0:
        for a in range(a2):
            gamatch2_text += f'''<g width="59" height="50" fill="none" transform = "translate({inital_x_a+59*a},320)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M37.9998 3C37.9998 1 32.4998 0 32.4998 0L26.4998 10.5C24.4998 10.5 23.4998 14.5 23.4998 14.5C23.4998 14.5 21.1664 16.5 20.9998 18C19.7998 18.4 11.4998 26.5 7.49983 30.5C0.429491 36.1562 0.468828 38.2577 0.496511 39.7366C0.498194 39.8265 0.499834 39.914 0.499831 40C2.99983 44 7.1665 44 9.99983 44C12.0245 45.4666 57.9998 22 57.9998 19.5C57.9998 17 57.1998 15.5 53.9998 9.5C50.7998 3.5 45.9998 1.33333 43.9998 1V5C40.3998 10.6 36.1665 10.6667 34.4998 10C34.4998 10 37.9998 5 37.9998 3ZM21.4998 37.5L27.4998 34.5C26.4998 32 33.4998 24 37.9998 20.5C41.5998 17.7 47.8331 10.8333 50.4998 7.5L49.4998 6C47.3507 11.5877 37.4422 19.0228 31.8444 23.2233C30.9305 23.9091 30.1314 24.5087 29.4998 25C25.8998 27.8 22.6664 34.5 21.4998 37.5ZM52.4999 9L52.9999 9.5C51.3332 12 46.4998 18 46.4998 18C46.4998 18 38.4999 27 39.9999 28L33.4998 31.5C33.4998 31.5 35.4998 26.5 38.9998 23.5C42.4998 20.5 49.4998 13 52.4999 9Z" fill="#33F000"/>
    <path d="M58 22.5L52.5 25.5L55 29L58.5 27.5L58 22.5Z" fill="#33F000"/>
    <path d="M49.5 27L44 30L46.5 33.5L50 32L49.5 27Z" fill="#33F000"/>
    <path d="M24.5 40L19 43L21.5 46L25.5 44L24.5 40Z" fill="#33F000"/>
    <path d="M17 43.5L11.5 45L14.5 49.5L18 48L17 43.5Z" fill="#33F000"/>
    </g>\n'''    

    # THIS IS THE SVG CODE

    svg_code =f"""<svg width="1088" height="1920" viewBox="0 0 1088 1920" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <text fill="white" font-family="Inter" font-size="55" font-weight="bold" x="95" y="55">Season 2022/2023 Achievements</text>

                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="35" x="345" y="135">Average Seasson Rating</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="50" x="480" y="200">{year_rating}</text>
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="35" x="600" y="200">rtg</text>

                    <rect x="{544-match_separation_half - 95}" y="220" width="95" height="79" fill="none"/>
                    {gamatch1_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="60" x="{544+match_separation_half}" y="280">{matches[0][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="30" x="{544+match_separation_half+140}" y="280">rtg</text>

                    <rect x="{544-match_separation_half - 95}" y="300" width="95" height="79" fill="none"/>
                    {gamatch2_text}
                    <text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="60" x="{544+match_separation_half}" y="360">{matches[1][3]}</text><text fill="#0FB916" font-family="Inter" font-weight="bold" font-size="30" x="{544+match_separation_half+140}" y="360">rtg</text>

                    <rect x="300" y="698.065" width="494" height="309.494" rx="15" fill="white"/>

                    <rect width="828" height="884" rx="40" transform="matrix(-1 0 0 1 974 408)" fill="#1D1D1D"/>
                    <text fill="white" font-family="Inter" font-size="40" font-weight="bold" x="420" y="460">This season stats</text>
                    <path d="M206.373 480.18H887.355" stroke="#525252" stroke-linecap="round"/>

                    {stats_text}
                </svg>"""


    with open(path+'svg.svg','w') as f:
        f.write(svg_code)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(path +"svg.svg")
    shape.image_data.save(path +"svg.png")
    

    background = cv2.imread(path+'images/background.png')
    overlay = cv2.imread(path+'svg.png', cv2.IMREAD_UNCHANGED)
    img_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Resources/'
    club1 = Image.open(img_path+f'Clubs/{matches[0][0]}.webp').convert("RGBA")
    club2 = Image.open(img_path+f'Clubs/{matches[1][0]}.webp').convert("RGBA")
    percentiles = Image.open(path+f'images/percentiles.png')

    #Background adjusting
    height, witdh, channels = background.shape
    scale = height / 1920
    old_width = witdh
    witdh = int(witdh / scale)
    width_diff = abs((witdh-1080)//2)
    background = cv2.resize(background,(witdh,1920))
    background = background[0:1920,width_diff:width_diff+1080]

    #Overlay adjusting
    height, witdh, channels = overlay.shape
    overlay = cv2.resize(overlay,(1080,1920))
    imgResult = cvzone.overlayPNG(background,overlay,[0,250])
    cv2.imwrite(path+'Video3(no clubs).png', imgResult)

    # Percentiles
    width, height = percentiles.size
    multiplier = width / 770
    height = int(height / multiplier)
    percentiles = percentiles.resize((770,height))
    percentile_offset = 560 - 770 // 2 
    percentiles = add_corners(percentiles,20)

    # Club adjusting
    club_size = 70

    width, height = club1.size
    scale = width / club_size
    height1 = int(height / scale)
    club1 = club1.resize((club_size,height1))
    width,height = club2.size
    scale = width / club_size
    height2 = int(height / scale)
    club2 = club2.resize((club_size,height2))

    imgResult = Image.open(path+'video3(no clubs).png')
    imgResult.paste(club1, (544-match_separation_half - club_size,(220-(height1-club_size)//2)+250), mask= club1)
    imgResult.paste(club2, (544-match_separation_half - club_size,(300-(height2-club_size)//2)+250), mask= club2)
    imgResult.paste(percentiles, (percentile_offset,percentile_height +320), mask= percentiles)
    imgResult.save(path+"Video-2.png")

    
    os.remove(path+"Video3(no clubs).png")
    os.remove(path+"svg.svg")
    os.remove(path+"svg.png")

def make_posts(path,player,youngster, Hook, matches, stats, info):
    make_ig_post1(path, youngster)
    make_ig_post2(path,player,info)
    make_ig_post3(path,matches,stats)
    make_video1(path,player)
    make_video2(path,player,info)
    make_video3(path,matches,stats)
    make_ig_story(path,player, Hook)
    create_vid()
