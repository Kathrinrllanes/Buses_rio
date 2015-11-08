
import pandas as pd
import datetime

def bus_departure_hour(initial_points_timestamp_list):
    list_departure_hours = []
    i = 0
    if len(initial_points_timestamp_list) >1:
        for i in range(0, len(initial_points_timestamp_list)-1):
            resto = datetime.datetime.strptime(initial_points_timestamp_list[i+1], "%d-%m-%Y %H:%M:%S")-datetime.datetime.strptime(initial_points_timestamp_list[i], "%d-%m-%Y %H:%M:%S")
            resto_total = resto.total_seconds()/60
            #si la diferencia entre los timestamp del omnibus en el putno supera los 40 minutos es q dio un viaje y regreso, sino lo supera es que se mantuvo ese tiempo esperando en el punto
            if (resto_total > 40):
                 list_departure_hours.insert(len( list_departure_hours),datetime.datetime.strptime(initial_points_timestamp_list[i], "%d-%m-%Y %H:%M:%S"))
        #siempre es necesario insertar el ultimo valor de la lista de "initial_points_timestamp" en la lista de  list_departure_hours 
        list_departure_hours.insert(len( list_departure_hours),datetime.datetime.strptime(initial_points_timestamp_list[i+1], "%d-%m-%Y %H:%M:%S"))
    elif len(initial_points_timestamp_list) == 1:
        list_departure_hours.insert(len( list_departure_hours),datetime.datetime.strptime(initial_points_timestamp_list[0], "%d-%m-%Y %H:%M:%S"))
    else:
        list_departure_hours = []
    return list_departure_hours

#Funcion que retorna el arreglo con las horas de llegada del omnibus al punto inicial/final del trayecto
def bus_arrive_hour(initial_points_timestamp_list):
    list_arrive_hours = []
    #siempre es necesario insertar el ultimo valor de la lista de "initial_points_timestamp" en la lista de leblon_departure_hours 
    if len(initial_points_timestamp_list) >1:
        list_arrive_hours.insert(len(list_arrive_hours),datetime.datetime.strptime(initial_points_timestamp_list[0], "%d-%m-%Y %H:%M:%S"))
        for i in range(0,  len(initial_points_timestamp_list)-1):
            resto = datetime.datetime.strptime(initial_points_timestamp_list[i+1], "%d-%m-%Y %H:%M:%S")-datetime.datetime.strptime(initial_points_timestamp_list[i], "%d-%m-%Y %H:%M:%S")
            resto_total = resto.total_seconds()/60
            if (resto_total > 40):
                list_arrive_hours.insert(len(list_arrive_hours),datetime.datetime.strptime(initial_points_timestamp_list[i+1], "%d-%m-%Y %H:%M:%S"))
    elif (len(initial_points_timestamp_list) == 1):
        list_arrive_hours.insert(len(list_arrive_hours),datetime.datetime.strptime(initial_points_timestamp_list[0], "%d-%m-%Y %H:%M:%S"))
    else:
        list_arrive_hours = []        
    return list_arrive_hours  

#Para convertir de formato timedelta para horas y minutos
def days_hours_minutes(travel_time):
    hours = travel_time.seconds//3600 
    minutes = (travel_time.seconds//60)%60
    #print '%d hours, %d minutes' % (hours,minutes)
    if minutes < 10:
        minutes = str(0)+str(minutes)
    return str(hours) + ":"+ str(minutes)

#Funcion que crea la tabla de viajes con los tiempos de viaje
def create_travel_table(name_A, arrive_array_A, departure_array_A, name_B, arrive_array_B, departure_array_B, bus_Id, bus_line):
    my_time_table = []   
    num_travel = 0    
    i = 0 #Cursor para moverme por el departure_array_A(arreglo q contiene las horas de salida del punto incial)   
    j = 0 #Cursor para moverme por el departure_array_B (arreglo q contiene las horas de salida del punto final)

    while (i<len(departure_array_A) and j< len(departure_array_B)):
        if (departure_array_A[i] < departure_array_B[j]):
            if(i+1 == len(departure_array_A)):
                direction = name_A + "_to_" + name_B
                departure_hour = departure_array_A[i]
                i = i +1
                arrive_hour = arrive_array_B[j]
                num_travel = num_travel +1
                travel_time = days_hours_minutes(arrive_hour - departure_hour)          
                my_time_table.insert(len(my_time_table), [bus_line, bus_Id, direction, departure_hour,arrive_hour, travel_time])

            elif ((i+1 < len(departure_array_A)) and (departure_array_B[j] < departure_array_A[i+1])):
                direction = name_A + "_to_" + name_B
                departure_hour = departure_array_A[i]
                i = i +1
                arrive_hour = arrive_array_B[j]
                num_travel = num_travel +1
                travel_time = days_hours_minutes(arrive_hour - departure_hour)          
                my_time_table.insert(len(my_time_table), [bus_line, bus_Id, direction, departure_hour,arrive_hour, travel_time])
            else: 
                i = i +1

        elif(departure_array_B[j] < departure_array_A[i]):
            if (j+1 == len(departure_array_B)):
                direction = name_B + "_to_" + name_A
                departure_hour = departure_array_B[j]
                j = j +1
                arrive_hour = arrive_array_A[i]
                num_travel = num_travel +1
                travel_time = days_hours_minutes(arrive_hour - departure_hour)          
                my_time_table.insert(len(my_time_table), [bus_line, bus_Id, direction, departure_hour,arrive_hour, travel_time])

            elif ((j+1 < len(departure_array_B)) and (departure_array_A[i] < departure_array_B[j+1])):
                direction = name_B + "_to_" + name_A
                departure_hour = departure_array_B[j]
                j = j +1
                arrive_hour = arrive_array_A[i]
                num_travel = num_travel +1
                travel_time = days_hours_minutes(arrive_hour - departure_hour)          
                my_time_table.insert(len(my_time_table), [bus_line, bus_Id, direction, departure_hour,arrive_hour, travel_time])
            else:
                j = j +1                

    #Construir el dataframe pasandole el array con todos los datos de los viajes   
    mydf = pd.DataFrame(my_time_table, columns=['Line', 'Bus_Id','Direction','Departure_Hour', 'Arrive_Hour', 'Travel_Time'])       
    return mydf  

#Funcion que crea la tabla de tiempo de viaje para cada bus_id de los que transitaron el el dia
def all_travel_table(line, punto_ini_coord_invertidas, name_punto_inicio, punto_fin_coord_invertidas, name_punto_final, array_busId):
    new_df = pd.DataFrame(columns=['Line', 'Bus_Id','Direction','Departure_Hour', 'Arrive_Hour', 'Travel_Time'])  
    for busId in array_busId:
        sorted_near_initial_points1 = near_points_to_origin(busId, punto_ini_coord_invertidas)
        sorted_near_final_points1 = near_points_to_origin(busId, punto_fin_coord_invertidas)
        initial_points_timestamp1 = sorted_near_initial_points1 ['timestamp']
        final_points_timestamp1 = sorted_near_final_points1 ['timestamp']
        #chequear si la lista initial_points_timestamp es diferente de vacio
        if len(initial_points_timestamp1) and len(final_points_timestamp1):
            vilaIsabel_departure_hours1 = bus_departure_hour(initial_points_timestamp1)
            first_point_departure_hour = bus_departure_hour (initial_points_timestamp1)
            last_point_departure_hour = bus_departure_hour (final_points_timestamp1)
            first_point_arrive_hour = bus_arrive_hour(initial_points_timestamp1)
            last_point_arrive_hour = bus_arrive_hour(final_points_timestamp1)
            my_time_table = create_travel_table(name_punto_inicio, first_point_arrive_hour, first_point_departure_hour, name_punto_final, last_point_arrive_hour, last_point_departure_hour, busId, line)
            new_df = new_df.append(my_time_table, ignore_index=True)
    return new_df


