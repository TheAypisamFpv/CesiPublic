import matplotlib.pyplot as plt
import math
'''Programme qui calcule la vitesse de la voiture en fonction de la pente et du looping'''



def get_air_density(Hauteur: float):
    return 1.225 * math.exp(-((7*9.81) / (2*1006*288.15))*Hauteur)



'''------------------------fonction qui demande a l'utilisateur si il veut afficher la vitesse en fonction du temps ou la position en Y en fonction du temps------------------------'''
def user_input():
    while True:
        user_input = input("Voulez vous afficher la vitesse en fonction du temps ou la position en Y en fonction du temps ? (vitesse/position): ")
        if user_input == 'vitesse':
            return 'vitesse'
        elif user_input == 'position':
            return 'position'
        else:
            print("Erreur, veuillez entrer 'vitesse' ou 'position'")




'''------------------------------------------------------------------------debut de la simulation------------------------------------------------------------------------'''
def simulation(piste_angle:int,hauteur_de_depart:float, plot:bool):
    """
    defaut: - piste_angle = 40
            - hauteur_de_depart = 0.93

    calcule la vitesse de la voiture en fonction des données donné, calcule effectué toutes les 0.001s
    """


    '''Coordonnées des points de la trajectoire'''

    '''si l'angle de la piste est a 0, alors on utilise les données du cas réel'''
    if piste_angle == 0:
        use_real_data = True

        '''hauteur de départ du ravin en mètre'''
        hauteur_de_depart = 1 # hauteur du ravin utilisé pour la hauteur de départ
        largeur_ravin = 9 # m
        
        '''diametre du looping en mètre'''
        diametre_looping = 12
        '''perimetre du looping en mètre'''
        perimetre = diametre_looping*math.pi

        pisteY = [hauteur_de_depart, hauteur_de_depart]
        pisteX = [0, 31]

        '''        point d'entré  section debut    ,     looping          , section fin / point de sortie '''
        loopingX = [pisteX[1],  pisteX[1] +(diametre_looping/2), pisteX[1] + perimetre, pisteX[1] + perimetre + (diametre_looping/2)]
        true_loopingX = [pisteX[1], pisteX[1] + diametre_looping/2, pisteX[1] + diametre_looping]
        loopingY = [pisteY[1], pisteY[1], pisteY[1], pisteY[1]]


        '''coordonnées du saut en Y et en X'''
        sautX = [true_loopingX[2] + largeur_ravin, true_loopingX[2] + largeur_ravin + 5]
        sautY = [0, 0]

    else:
        use_real_data = False

        '''hauteur de départ du ravin en mètre'''
        largeur_ravin = 0.7 # m
        
        '''diametre du looping en mètre'''
        diametre_looping = 0.23
        '''perimetre du looping en mètre'''
        perimetre = diametre_looping*math.pi
    
        pisteY = [hauteur_de_depart+0.1, 0.1]
        pisteX = [0, (pisteY[0] - 0.1) / math.sin(math.radians(piste_angle))]   #simule que la piste est plate 
    
        # angle_piste = 40 # °

        '''diametre du looping en mètre'''
        diametre_looping = 0.23
        '''perimetre du looping en mètre'''
        perimetre = 0.23*math.pi
        '''simulle que le looping est plat, d'une longueur du permimetre du looping'''


        '''        point d'entré  section debut    ,     looping          , section fin / point de sortie '''
        loopingX = [pisteX[1],  pisteX[1] +(diametre_looping/2), pisteX[1] + perimetre, pisteX[1] + perimetre + (diametre_looping/2)]
        true_loopingX = [pisteX[1], pisteX[1] + diametre_looping/2, pisteX[1] + diametre_looping]
        loopingY = [pisteY[1], pisteY[1], pisteY[1], pisteY[1]]


        '''coordonnées du saut en Y et en X'''
        sautX = [loopingX[3] + largeur_ravin, loopingX[3] + largeur_ravin + 2]
        sautY = [0, 0]



    if plot :
        '''demande a l'utilisateur si le graphique du la pente affiche la vitesse en fonction du temps ou de la position en Y en fonction du temps'''
        input_ = user_input()


    print('--------------------\nSimulation en cours...\n |')
    '''------------------------initialisation des variables------------------------'''

    '''constante gravitationnelle'''
    g = 9.81 # m/s²

    if use_real_data:
        '''initialisation des variables de la voiture'''
        voiture = {'X': pisteX[0], 'Y': pisteY[0], 'vitesse': 0}
        '''initialisation des variables de la simulation'''
        dt = 0.001 # s  

        '''coefficient de trainée de l'air'''
        Cx = 0.3  # (0.04 pour la version miniature, 0.3 pour la version réelle)
        Cx_ravin = 0.3 # (0.001 pour la version miniature, 0.3 pour la version réelle)

        '''coefficient de frottement de la route'''
        Ur = 0.01 # (0.002 pour la version miniature, 0.01 pour la version réelle)

        '''surface de la voiture'''
        surface = 1.94*1.35 # m² (3.12**-4 pour la version miniature, 1.94*1.35 m² pour la version réelle)

        '''poid de la voiture'''
        poid = 1760 * g # N (0.093 pour la version miniature, 1760 kg pour la version réelle)

    else:
        '''initialisation des variables de la voiture'''
        voiture = {'X': pisteX[0], 'Y': pisteY[0], 'vitesse': 0}
        '''initialisation des variables de la simulation'''
        dt = 0.001 # s

        '''coefficient de trainée de l'air'''
        Cx = 0.04  # (0.04 pour la version miniature, 0.3 pour la version réelle)
        Cx_ravin = 0.001 # (0.001 pour la version miniature, 0.3 pour la version réelle)

        '''coefficient de frottement de la route'''
        Ur = 0.002 # (0.002 pour la version miniature, 0.01 pour la version réelle)

        '''surface de la voiture'''
        surface = 3.12**-4 # m² (3.12**-4 pour la version miniature, 1.94*1.35 m² pour la version réelle)

        '''poid de la voiture'''
        poid = 0.093 * g # N (0.093 pour la version miniature, 1760 kg pour la version réelle)
        

    '''densité de l'air au niveau de la mer'''
    air_density = get_air_density(0)

    '''----------initialisation des logs pour en faire des graphes----------'''
    '''(1er element est None pour qu'il n'y ai pas d'erreur lors de la premiere boucle)'''
    LOG_vitesse_piste = [None]
    LOG_temps_piste = [0]
    LOG_positionY_piste = [pisteY[0]]
    LOG_positionX_piste = [pisteX[0]]

    
    crash = False



    '''------------------------------------------------début de la simulation pour la pente------------------------------------------------'''
    print(' |->Simulation de la pente...')
    while voiture['X'] <= pisteX[1] and not crash:
        '''la pente etant une droite commencant a 0, on peut calculer la hauteur en fonction de la position en X'''
        voiture['Y'] = (1 - voiture['X'] / pisteX[1]) * (pisteY[0]-pisteY[1]) + pisteY[1]

        '''calcule vitesse formule pente'''
        if use_real_data :
            a_constant = 8
        else:
            a_constant = math.sin(math.radians(piste_angle)) * g  # m/s²

        '''calcul de la force de frottement de l'air'''
        air_drag = (1/2 * air_density * surface * Cx * (voiture['vitesse']**2))/poid  # m/s²
        
        '''calcul de la force de frottement de la route'''
        road_drag = g * Ur  # m/s²
       
        '''calcul de l'accélération'''
        a = a_constant -(air_drag + road_drag)  # m/s²
        # print(f'DEBUG: a = {a:.4f} m/s², a_constant = {a_constant:.4f} m/s², air_drag = {air_drag:.4f} m/s², road_drag = {road_drag:.4f} m/s², vitesse = {voiture["vitesse"]:.4f} m/s, position = {voiture["X"]:.4f} m')

        '''calcul de la vitesse et de la position en X'''
        voiture['vitesse'] += a*dt
        voiture['X'] += voiture['vitesse']*dt

        '''ajout des données dans les logs'''
        LOG_vitesse_piste.append(voiture['vitesse'])
        LOG_positionY_piste.append(voiture['Y'])
        LOG_positionX_piste.append(voiture['X'])
        LOG_temps_piste.append(LOG_temps_piste[-1]+dt)

    
    if not crash: print(f' |  |->fin de la simulation de la pente, vitesse finale = {voiture["vitesse"]:.4f} m/s')

    '''------------------------------------------------fin de la simulation pour la pente------------------------------------------------'''





    ''' ------------------------------------------------debut de la simulation du looping------------------------(parties plates avant et après sont pris en compte)------------------------'''

    LOG_vitesse_looping = [LOG_vitesse_piste[-1]]
    LOG_temps_looping = [LOG_temps_piste[-1]]
    LOG_positionY_looping = [pisteY[-1]]
    LOG_positionX_looping = [LOG_positionX_piste[-1]]
    
    voiture['X'] = true_loopingX[0]
    '''------------entrée------------'''
    if not crash: print(" |\n |->Simulation de l'entrée du looping (1ere partie plate)...")
    a = LOG_vitesse_piste[-1] # m/s²
    while voiture['X'] <= true_loopingX[1] and not crash:

        '''calcule de la trainée de l'air'''
        air_drag = (1/2 * air_density * surface * Cx * (voiture['vitesse']**2))/poid  # m/s²

        '''calcule des forces de frottement de la route'''
        road_drag = g * Ur  # m/s²

        '''calcule de l'accélération'''
        a = -(air_drag + road_drag)  # m/s²

        '''calcule de la vitesse et de la position en X'''
        voiture['vitesse'] += a*dt
        voiture['X'] += voiture['vitesse']*dt

        '''calcule de la position en Y'''
        voiture['Y'] = loopingY[0] #position en Y consante car cette partie est plate

        '''ajout des données dans les logs'''
        LOG_vitesse_looping.append(voiture['vitesse'])
        LOG_positionY_looping.append(voiture['Y'])
        LOG_positionX_looping.append(voiture['X'])
        LOG_temps_looping.append(LOG_temps_looping[-1]+dt)

    if not crash: print(f' |  |->fin de la simulation de l\'entrée du looping, vitesse finale = {voiture["vitesse"]:.4f} m/s')





    '''------------Debut looping------------'''
    T_entrée_looping = len(LOG_temps_looping)+1

    if not crash: print(" |\n |->Simulation du looping...")
    while voiture['X'] <= loopingX[2] and not crash:

        if voiture['vitesse'] <= 0:
            print(f' |  |->vitesse inferieur ou égale a 0, la voiture tombe du looping')
            print(" |\n |->simulation annulee pour cause d'un crash de la voiture")
            crash = True

        '''calcule vitesse formule looping'''
        alpha = (voiture["X"]-loopingX[1])/(loopingX[2]-loopingX[1]) * (-360)

        '''calcule de l'accélération du a la gravité (alpha change de 0 a -360 pour simuler la courbe du looping)'''
        alpha_R = math.radians(alpha)  # rad
        a_g = g * math.sin(alpha_R)  # m/s²

        '''calcule de la position X et Y en fonciton de alpha_R'''
        voiture['Y'] = (1-math.sin(alpha_R + math.radians(90))) * diametre_looping/2 + loopingY[1]
        position_X = (-math.cos(alpha_R - math.radians(90))) * diametre_looping/2 + true_loopingX[1]

        '''calcule des forces de frottement de la route'''
        road_drag = g * Ur  # m/s²
        air_drag = (1/2 * air_density * surface * Cx * (voiture['vitesse']**2))/poid  # m/s²

        '''calcule de l'accélération'''
        a = a_g -(air_drag + road_drag)  # m/s²

        '''calcule de la vitesse et de la position en X'''
        voiture['vitesse'] += a*dt
        voiture['X'] += voiture['vitesse']*dt
        

        '''ajout des données dans les logs'''
        LOG_vitesse_looping.append(voiture['vitesse'])
        LOG_temps_looping.append(LOG_temps_looping[-1]+dt)
        LOG_positionY_looping.append(voiture['Y'])
        LOG_positionX_looping.append(position_X)

    if not crash: print(f' |  |->fin de la simulation du looping, vitesse finale = {voiture["vitesse"]:.4f} m/s')





    '''------------Sortie du looping------------'''
    T_sortie_looping = len(LOG_temps_looping)+1
    voiture['X'] = true_loopingX[1]

    if not crash: print(" |\n |->Simulation de la sortie du looping (2nd partie plate)...")
    while voiture['X'] <= true_loopingX[2] and not crash:

        '''calcule de la trainée de l'air'''
        air_drag = (1/2 * air_density * surface * Cx * (voiture['vitesse']**2))/poid  # m/s²

        '''calcule de la trainée de la route'''
        road_drag = g * Ur  # m/s²

        '''calcule de l'accélération'''
        a = -(air_drag + road_drag)  # m/s²

        '''calcule de la vitesse et de la position en X'''
        voiture['vitesse'] += a*dt
        voiture['X'] += voiture['vitesse']*dt

        '''calcule de la position en Y'''
        voiture['Y'] = loopingY[3]

        '''ajout des données dans les logs'''
        LOG_vitesse_looping.append(voiture['vitesse'])
        LOG_temps_looping.append(LOG_temps_looping[-1]+dt)
        LOG_positionY_looping.append(voiture['Y'])
        LOG_positionX_looping.append(voiture['X'])

    

    if not crash: print(f' |  |->fin de la simulation de la sortie du looping, vitesse finale = {voiture["vitesse"]:.4f} m/s')

    '''------------------------------------------------fin de la simulation du looping------------------------------------------------'''





    '''------------------------------------------------debut de la simulation du saut (ravin)------------------------------------------------'''
    LOG_vitesse_saut = [LOG_vitesse_looping[-1]]
    LOG_temps_saut = [LOG_temps_looping[-1]]
    LOG_positionY_saut = [loopingY[3]]
    LOG_positionX_saut = [true_loopingX[2]]

    if not crash: print(" |\n |->Simulation du saut...")

    on_ground = False

    voiture['Y'] = loopingY[3]
    Vy = 0

    '''utilisation d'un Cx plus faible (Cx_ravin)'''
    while voiture['X'] <= sautX[1] and not crash:

        road_drag = 0
        ay = -g
        Vy += ay*dt

        '''calcule de la position en Y'''
        voiture['Y'] += Vy*dt

        '''si la voiture est a la verticale de la route (endroit ou elle doit atterir)'''
        if voiture['X'] >= sautX[0]:

            '''si la voiture est au sol, on la remet ay, Vy et Y a 0 pour eviter les erreurs de calcul'''
            if voiture['Y'] <= 0:
                voiture['Y'] = 0
                ay = 0
                Vy = 0

                '''calcule des forces de frottement de la route'''
                road_drag = g * Ur  # m/s²

                '''on enregistre la position de la voiture lorsqu'elle touche le sol pour l'afficher sur le graphique'''
                if on_ground == False:
                    on_ground = True
                    T_on_ground = int((LOG_temps_saut[-1] - LOG_temps_saut[0])/dt)
                    print(f' |  |-> la voiture a atteri au sol, position X = {voiture["X"]:.4f} m')

        else:
            '''la voiture est en dessous de la route, elle s'est donc crashée'''
            if voiture['Y'] <= 0:
                crash = True
                '''affichage de la position x de la voiture lorsqu'elle s'est crashée'''
                print(f' |  |-> la voiture s\'est crashée, elle a atteint Y=0 a X = {voiture["X"]-true_loopingX[2]:.4f} m (la route est a X = {sautX[0]-loopingX[3]:.4f} m)')
                print(f' |\n |->simulation annulée pour cause d\'un crash de la voiture')
            

           
        '''calcule de la trainée de l'air'''
        air_drag = (1/2 * air_density * surface * Cx_ravin * (voiture['vitesse']**2))/poid  # m/s²

        '''calcule de la deceleration du aux forces de frottement de la route et de l'air'''
        ax = - (air_drag + road_drag)  # m/s²

        '''calcule de la vitesse et de la position en X'''
        voiture['vitesse'] += ax*dt
        voiture['X'] += voiture['vitesse']*dt

        

        '''ajout des données dans les logs'''
        LOG_vitesse_saut.append(voiture['vitesse'])
        LOG_temps_saut.append(LOG_temps_saut[-1]+dt)
        LOG_positionY_saut.append(voiture['Y'])
        LOG_positionX_saut.append(voiture['X'])

    if not crash: print(f" |  |->fin de la simulation du saut, vitesse finale = {voiture['vitesse']:.4f} m/s")

    if not crash: print(f" |\n Simulation terminée, vitesse finale = {voiture['vitesse']:.4f} m/s")

    '''------------------------------------------------fin de la simulation du saut (ravin)------------------------------------------------'''

    FULL_LOG_VITESSE = LOG_vitesse_piste + LOG_vitesse_looping + LOG_vitesse_saut
    FULL_LOG_POSITIONY = LOG_positionY_piste + LOG_positionY_looping + LOG_positionY_saut
    FULL_LOG_POSITIONX = LOG_positionX_piste + LOG_positionX_looping + LOG_positionX_saut
    FULL_LOG_TEMPS = LOG_temps_piste + LOG_temps_looping + LOG_temps_saut

    print("\naffichage des graphes...\n--------------------")

    '''------------------------------------------------affichage des graphes------------------------------------------------'''
    if plot:
        figure, axis = plt.subplots(2, 2)

        ''' !!! Modifiez 'font.size' si la police d'écriture n'est pas adapté a votre écran !!! '''
        plt.rcParams.update({'font.size': 10}) #defaut = 10


        ''' graphe de la vitesse ou de la position en fonction du temps (sur demande de l'utilisateur)'''
        if input_ == 'vitesse':
            figure.suptitle(f"Simulation de la voiture, vitesse en fonction du temps (poid = {poid/g:.3f}kg, surface = {surface:.3f}m², Cx = {Cx}, Cx_ravin = {Cx_ravin:.3f}, Ur = {Ur}, angle de la piste = {piste_angle}°, hauteur de départ = {hauteur_de_depart}m (dela hauteur de la pente))\n(Axes X en s, Axes Y en m/s)")

            '''graphes de la vitesse sur le plan incliné en fonction du temps'''
            axis[0, 0].plot(LOG_temps_piste, LOG_vitesse_piste, 'b')
            axis[0, 0].set_title("Vitesse sur le plan incliné en fonction du temps")


            '''graphes de la vitesse sur le looping (parties plates avant et après) en fonction du temps'''
            axis[0, 1].plot(LOG_temps_looping, LOG_vitesse_looping, 'b')
            axis[0, 1].plot(LOG_temps_looping[T_entrée_looping:T_sortie_looping], LOG_vitesse_looping[T_entrée_looping:T_sortie_looping], 'r')
            axis[0, 1].set_title("Vitesse sur le looping (partie rouge = looping)")


            '''graphes de la vitesse sur le saut en fonction du temps'''
            axis[1, 0].plot(LOG_temps_saut ,LOG_vitesse_saut, 'b')
            if not crash:

                '''graphe de la vitesse sur le saut si la voiture ne s'est pas crashée (partie rouge = voiture au sol) en fonction du temps'''
                axis[1, 0].plot(LOG_temps_saut[T_on_ground::], LOG_vitesse_saut[T_on_ground::], 'r')
                axis[1, 0].set_title(f"Vitesse sur le saut (partie rouge = voiture au sol) (Cx_ravin = {Cx_ravin:.3f})")
            else:
                
                '''graphe du point de crash'''
                axis[1, 0].plot(LOG_temps_saut[-1], LOG_vitesse_saut[-1], 'ro')    
                axis[1, 0].set_title(f"Vitesse sur le saut (point rouge = crash de la voiture) (Cx_ravin = {Cx_ravin:.3f})")


            '''graphes de la vitesse sur l'ensemble'''
            axis[1, 1].plot(FULL_LOG_TEMPS, FULL_LOG_VITESSE, 'b')
            axis[1, 1].set_title("Vitesse sur l'ensemble en fonction de la position X")

        elif input_ == 'position':

            figure.suptitle(f"Simulation de la voiture, Y en fonction de X (poid = {poid/g:.3f}kg, surface = {surface:.3f}m², Cx = {Cx}, Cx_ravin = {Cx_ravin:.3f}, Ur = {Ur}, angle de la piste = {piste_angle}°, hauteur de départ = {hauteur_de_depart}m (dela hauteur de la pente))\n(Axes X en m, Axes Y en m)")

            '''graphes de la position Y sur le plan incliné en fonction de X'''
            axis[0, 0].plot(LOG_positionX_piste, LOG_positionY_piste, 'b')
            axis[0, 0].axis('equal')
            axis[0, 0].set_title("Position en Y de la voiture sur le plan incliné en fonction de la position X")

            '''graphes de la position Y sur le looping (parties plates avant et après) en fonction de X''' 
            interval = 5          
            axis[0, 1].plot(LOG_positionX_looping[0:T_entrée_looping+1:interval], LOG_positionY_looping[0:T_entrée_looping+1:interval], 'b+')
            axis[0, 1].plot(LOG_positionX_looping[T_sortie_looping::interval], LOG_positionY_looping[T_sortie_looping::interval], 'b+')
            '''graphe de la position Y en fonction de la position X dans le looping, prise en compte que d'une donnée sur 3'''
            axis[0, 1].plot(LOG_positionX_looping[T_entrée_looping:T_sortie_looping+1:interval], LOG_positionY_looping[T_entrée_looping:T_sortie_looping+1:interval], 'r+')
            # axis[0, 1].plot(LOG_positionX_looping[T_entrée_looping:T_sortie_looping], LOG_positionY_looping[T_entrée_looping:T_sortie_looping], 'r+')

            axis[0, 1].axis('equal')
            axis[0, 1].set_title("Position en Y de la voiture sur le looping (partie rouge = looping)")

            '''graphes de la position Y sur le saut en fonction de X'''
            axis[1, 0].plot(LOG_positionX_saut, LOG_positionY_saut, 'b')
            if not crash:

                '''graphe de la position Y sur le saut si la voiture ne s'est pas crashée (partie rouge = voiture au sol) en fonction de X'''
                axis[1, 0].plot(LOG_positionX_saut[T_on_ground::], LOG_positionY_saut[T_on_ground::], 'r')
                axis[1, 0].set_title(f"Position en Y de la voiture sur le saut (partie rouge = voiture au sol) (Cx_ravin = {Cx_ravin:.3f})")
            else:
                    
                    '''graphe du point de crash'''
                    axis[1, 0].plot(LOG_positionX_saut[-1], LOG_positionY_saut[-1], 'ro')
                    axis[1, 0].set_title(f"Position en Y de la voiture sur le saut (point rouge = crash de la voiture) (Cx_ravin = {Cx_ravin:.3f})")
            axis[1, 0].axis('equal')

            '''graphes de la position Y sur l'ensemble en fonction de X'''
            axis[1, 1].plot(FULL_LOG_POSITIONX, FULL_LOG_POSITIONY, 'b')
            axis[1, 1].plot(LOG_positionX_looping[T_entrée_looping:T_sortie_looping], LOG_positionY_looping[T_entrée_looping:T_sortie_looping], 'r')
            if not crash:axis[1, 1].plot(LOG_positionX_saut[T_on_ground::], LOG_positionY_saut[T_on_ground::], 'r')
            axis[1, 1].axis('equal')
            axis[1, 1].set_title("Position en Y de la voiture sur l'ensemble en fonction de la position X")
            

        plt.show()

    '''------------------------------------------------fin du programme------------------------------------------------'''
    return crash



if __name__ == "__main__":
    simulation(piste_angle=40, hauteur_de_depart=0.93, plot=True) # (angle de la piste a 40° et hauteur de depart a 0.93m pour la version miniature, 0° et 0m pour la version réelle)

