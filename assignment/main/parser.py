# Function to Convert Angle to Direction
def angle_to_direction(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return (arr[(val % 16)])      

# Function Parse Wind info and Seprates Gusting, knots and Calculates the Direction
def parse_wind_info(wind:str):
    if wind == "":
        return "No Data Available"
    gust=""
    response_info=""
    if 'G' in wind:
                gust=wind[wind.index('G')+1:-2]
                wind=wind[:wind.index('G')]+'KT'
                speed=int(wind[3:-2])
                # Converting the Angle into Direction
                direction = angle_to_direction(int(wind[0:3]))              
                response_info=f'{direction} at {round((float(speed) * 1.151))} mph ({speed} knot) {gust} gusting to {speed} knots'
                return response_info

    speed=int(wind[3:-2])
    direction = angle_to_direction(int(wind[0:3]))
    response_info =f'{direction} at {round((float(speed) * 1.151))} mph ({speed} knot)'
    return response_info
    

# Function Parse the Temperature Info
def parse_temperature_info(temp:str):
    if temp == "":
        return "No Data Available"
    response=""
    temperature=0
    string = temp.split('/')
    vals=[val for val in string[0] if val.isdigit()]
    vals = int(''.join(vals))
    if 'M' in string[0]:
        # Adding Negative Sign to the Integer
        temperature = -abs(vals)
    else:
        temperature = vals 
    #Converting to Farenheit
    farenheit = (temperature * 1.8) + 32  
    response = f'{temperature} C ({int(farenheit)}F)'
    return response

#Function Responsbile for Parsing the Wether Info
def wether_report(data:str):
    temps=""
    winds=""
    data = data.split()
    for bit in data:
        if '/' in bit:
            temps=bit
        if 'KT' in bit:
            winds=bit

    #Calling temperature and Wind Parsing functions
    response =parse_temperature_info(temps)
    wind_response = parse_wind_info(winds)
    wetherReport = {
        "station" : data[2],
        "last_observation" : data[0] + " at " + data[1] + " G.M.T",
        "temperature": response,
        "wind" : wind_response
    }
    return wetherReport
    