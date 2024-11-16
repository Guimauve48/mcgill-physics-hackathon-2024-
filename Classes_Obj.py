#kg par m^3
#1 mini = 1kg
#all mass in kg
#all coord in meters
import math
PI = math.pi

class CubeInfini:
    #Create a point with a mass and position
    def __init__(self, position_x, position_y, position_z, volume, arrete):
        self.volume = volume
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.arrete = arrete
    def __str__(self):
        return f'{self.position_x}, {self.position_y}, {self.position_z}'

    #To take back position of the point
    def position(self):
        return [self.position_x, self.position_y, self.position_z]
    
    def arret_cube(self):
        return self.volume ** (1/3)
    

class Prisme:
    def __init__(self, x, y, z, largeur, longuer, hauteur, masse):
        self.x = x 
        self.y = y
        self.z = z
        self.largeur = largeur
        self.longuer = longuer
        self.hauteur = hauteur
        self.masse = masse


    def volume_tot(self):
        return (self.largeur * self.longuer * self.hauteur)
    
    ################################
    def tot_num_cube(self):
        return self.masse
    
    def volume_1_cube(self):
        return self.volume_tot() / self.tot_num_cube()
    
    def arrete_cube(self):
        return self.volume_1_cube() ** (1/3)

    #################################
    def recantgle_base(self):
        point_1 = [self.x, self.y, self.z]
        point_2 = [self.x + self.largeur, self.y, self.z]
        point_3 = [self.x, self.y + self.longuer, self.z]
        point_4 = [self.x + self.largeur, self.y + self.longuer, self.z]
        list_points_plan_base = [point_1, point_2, point_3, point_4]
        return list_points_plan_base
    
    def point_milieu_tot(self):
        point_milieu = [(self.x + (self.largeur / 2)), (self.y + (self.longuer / 2)), (self.z + (self.hauteur / 2))]
        return point_milieu

    def position_milieu_cube_centre(self):
        centre = self.point_milieu_tot()
        x_cube_centre = centre[0] + (self.arrete_cube() / 2)
        y_cube_centre = centre[1] + (self.arrete_cube() / 2)
        z_cube_centre = centre[2] + (self.arrete_cube() / 2)
        centre = [x_cube_centre, y_cube_centre, z_cube_centre]
        return centre
    
    def num_cube_largeur_longuer_hauteur_1_cadrant(self):
        #cube_milieu = self.position_milieu_cube_centre()
        position = (self.arrete_cube() / 2)

        num_cube_largeur = 0
        num_cube_longueur = 0
        num_cube_hauteur = 0

        while (position) <= (self.largeur / 2):
            position += self.arrete_cube()
            num_cube_largeur += 1

        position = (self.arrete_cube() / 2)

        while (position) <= (self.largeur / 2):
            position += self.arrete_cube()
            num_cube_longueur += 1
        
        position = (self.arrete_cube() / 2)
        while (position) <= (self.largeur / 2):
            position += self.arrete_cube()
            num_cube_hauteur += 1

        list_num_cube = [num_cube_largeur, num_cube_longueur, num_cube_hauteur]
        return list_num_cube

    def trouver_point_cube_cadrant_1(self):
        num_largeur = self.num_cube_largeur_longuer_hauteur_1_cadrant()[0]
        num_longueur = self.num_cube_largeur_longuer_hauteur_1_cadrant()[1]
        num_hauteur = self.num_cube_largeur_longuer_hauteur_1_cadrant()[2]

        list_tot_point = []
        point_milieu = self.position_milieu_cube_centre()
        x_init = point_milieu[0]
        y_init = point_milieu[1]
        z_init = point_milieu[2]

        adding = self.arrete_cube()
        for i in range(num_largeur):
            position_x = x_init + (i * adding)
            for j in range(num_longueur):
                position_y = y_init + (j * adding)
                for k in range(num_hauteur):
                    position_z = z_init + (k * adding)
                    list_tot_point.append([position_x, position_y, position_z])
        return list_tot_point
    
    def trouver_point_cube_cadrant2(self):
        list_point_cadrant_2 = self.trouver_point_cube_cadrant_1()[:]
        transverser = (self.largeur) / 2
        for point in list_point_cadrant_2:
            point[0] = point[0] - transverser

        return list_point_cadrant_2
    
    def create_down_candrants_from_combine_cadrant_1_et_2(self):
        list_cadran_1 = self.trouver_point_cube_cadrant_1()[:]
        list_cadran_2 = self.trouver_point_cube_cadrant2()[:]
        list_quart_forme = list_cadran_1 + list_cadran_2
        transverser = (self.largeur) / 2

        for element in list_quart_forme:
            element[2] = element[2] - transverser
        return list_quart_forme
    
    def create_total_points_for_prisme(self):
        down_qurater = self.create_down_candrants_from_combine_cadrant_1_et_2()[:]
        up_quarter = self.trouver_point_cube_cadrant_1()[:] + self.trouver_point_cube_cadrant2()[:]
        half_solid = down_qurater + up_quarter
        transverser = (self.largeur) / 2
        for element in half_solid:
            element[1] = element[1] - transverser
        return half_solid
    
    def complete_list_point_in_prisme(self):
        down_qurater = self.create_down_candrants_from_combine_cadrant_1_et_2()[:]
        up_quarter = self.trouver_point_cube_cadrant_1()[:] + self.trouver_point_cube_cadrant2()[:]
        half_solid = down_qurater + up_quarter
        second_half_solid = self.create_total_points_for_prisme()[:]
        return half_solid + second_half_solid

    def create_liste_cubeinfini_object(self):
        points = self.complete_list_point_in_prisme()[:]
        list_obj_cube = [CubeInfini(points[0], points[1], points[2], self.volume_1_cube(), self.arrete_cube()) for p in points]
        return list_obj_cube


class Cone:
    def __init__(self, x_center, y_center, z_center, rayon_bas, rayon_haut, hauteur, masse):
        self.x_center = x_center
        self.y_center = y_center
        self.z_center = z_center
        self.rayon_bas = rayon_bas
        self.rayon_haut = rayon_haut
        self.hauteur = hauteur
        self.masse = masse

    def volume_tot(self):
        return round((PI/3) * (self.hauteur) * ((self.rayon_bas ** 2) + (self.rayon_haut ** 2) + (self.rayon_bas * self.rayon_haut)))
    
    def tot_num_cube(self):
        return self.masse
    
    def volume_1_cube(self):
        return self.volume_tot() / self.tot_num_cube()
    
    def arrete_cube(self):
        return round(self.volume_1_cube() ** (1/3), 5)
    
    def find_all_position_of_z(self):
        starting_z = self.arrete_cube() / 2
        number_cube_en_z = 0
        list_z = []
        while starting_z <= self.hauteur:
            list_z.append(starting_z)
            starting_z += self.arrete_cube()
            number_cube_en_z += 1
        return list_z


    def find_pente_entre_rayon(self):
        rayon_haut = self.rayon_haut
        rayon_bas = self.rayon_bas
        if rayon_haut == rayon_bas:
            return 0
        y_1 = self.hauteur
        y_2 = 0
        x_1 = 0
        x_2 = (rayon_bas - rayon_haut)
        pente_droite_entre_rayon = (y_1 - y_2) / (x_1 - x_2)
        return pente_droite_entre_rayon
    
    def find_rayon_chaque_z(self):
        list_des_z = self.find_all_position_of_z()[:]
        rayon_haut = self.rayon_haut
        rayon_bas = self.rayon_bas
        pente = self.find_pente_entre_rayon()
        liste_z_with_r = []
        for z in list_des_z:
            if pente == 0:
                rayon = rayon_bas
            elif pente < 0:
                rayon = (z - self.hauteur)/pente
                rayon += rayon_haut
            elif pente > 0:
                rayon = z/pente
                rayon += rayon_bas
            liste_z_with_r.append([z, rayon])
        return liste_z_with_r
    
    def position_first_cube_per_innercircle(self):
        position_x = self.x_center + (self.arrete_cube() / 2)
        position_y = self.y_center + (self.arrete_cube() / 2)
        return [position_x, position_y]
    
    def position_all_center_of_circle_r_and_num_cube_in_r(self):
        list_des_z = self.find_rayon_chaque_z()[:]
        liste_complete = []
        for z in list_des_z:
            rayon = z[1]
            if (self.arrete_cube() / 2) > rayon:
                num_cube = 0
            else: 
                num_cube = (rayon + (self.arrete_cube() / 2))//(self.arrete_cube())
            position_x_y = self.position_first_cube_per_innercircle()[:]
            liste_a_append = position_x_y + z + [num_cube]
            liste_complete.append(liste_a_append)
        return liste_complete
    
    

    def trouver_point_pour_cercle_premier_cadrant(self, list_info):
        x = list_info[0]
        y = list_info[1]
        z = list_info[2]
        rayon = list_info[3]
        list_cadrant_1 = []
        while y**2 <= (rayon ** 2) - (x ** 2):
            while x**2 <= (rayon ** 2) - (y ** 2):
                list_adding = [x,y] + [z]
                list_cadrant_1.append(list_adding)
                x += (self.arrete_cube())
            x = list_info[0]
            y += (self.arrete_cube())
        return list_cadrant_1
    
    list_test = [1.816675, 1.816675, 0.816675, 11.183325, 7.0]
    def find_second_cadrant_left(self, list):
        point_1_cadrant = self.trouver_point_pour_cercle_premier_cadrant(list)
        point_2e_cadrant = point_1_cadrant[:]
        for element in point_2e_cadrant:
            x = (2 * self.x_center) - element[0]
            element[0] = x
        return point_2e_cadrant
    
    def demi_cercle(self, list):
        quarter_1 = self.trouver_point_pour_cercle_premier_cadrant(list)
        quarter_2 = self.find_second_cadrant_left(list)
        return quarter_1 + quarter_2


    def other_half_circle(self, list):
        demi_cercle = self.demi_cercle(list)
        demi_cercle_a_return = demi_cercle[:]
        for element in demi_cercle_a_return:
            y = (2 * self.y_center) - element[1]
            element[1] = y
        return demi_cercle_a_return
    
    def tot_cericle_at_z(self, list):
        half_1 = self.demi_cercle(list)
        half_2 = self.other_half_circle(list)
        return half_1 + half_2
    
    def trouver_tous_les_points_cone(self):
        list_complete_cone = []
        list_tous_centre = self.position_all_center_of_circle_r_and_num_cube_in_r()
        for list_a_etudier in list_tous_centre:
            list_cercle_at_given_z = self.tot_cericle_at_z(list_a_etudier)
            list_complete_cone = list_complete_cone + list_cercle_at_given_z
        return list_complete_cone

class Ellipsoide:
    def __init__(self, x, y, z, rX, rY, rZ, masse):
        self.x_init = x
        self.y_init = y
        self.z_init = z
        self.rayon_X = rX
        self.rayon_Y = rY
        self.rayon_Z = rZ
        self.masse = masse

    def volume_tot(self):
        return (4/3) * (PI) * (self.rayon_X * self.rayon_Y * self.rayon_Z)
    
    def tot_num_cube(self):
        return self.masse
    
    def volume_1_cube(self):
        return self.volume_tot() / self.tot_num_cube()
    
    def arrete_cube(self):
        return round(self.volume_1_cube() ** (1/3), 5)
    
    def point_milieu_cube(self):
        x_intitial = self.x_init + (self.arrete_cube() / 2)
        y_intitial = self.y_init + (self.arrete_cube() / 2)
        z_intitial = self.z_init + (self.arrete_cube() / 2)
        return [x_intitial, y_intitial, z_intitial]

    def trouver_tous_points_z(self):
        point_ini = self.point_milieu_cube()
        x_test = point_ini[0]
        y_test = point_ini[1]
        z_test = point_ini[2]
        max = self.rayon_Z
        list_point_milieu = []
        while z_test <= max:
            list_point_milieu.append([x_test, y_test, z_test])
            z_test += self.arrete_cube()
        return list_point_milieu

    def trouver_tous_points_1er_cadrant(self, list):
        position_x = list[0]
        position_y = list[1]
        position_z = list[2]
        x_init = self.x_init
        y_init = self.y_init
        list_cadrant_1 = []
        while (position_y - y_init) **2 <= ((self.rayon_Y) ** 2) * (1 - (((position_x - x_init) ** 2) / ((self.rayon_X) ** 2))):
            while (position_x - x_init) **2 <= ((self.rayon_Y) ** 2) * (1 - (((position_y - y_init) ** 2) / ((self.rayon_X) ** 2))):
                adding_point = [position_x, position_y, position_z]
                list_cadrant_1.append(adding_point)
                position_x += (self.arrete_cube())
            position_x = list[0]
            position_y += (self.arrete_cube())
        return list_cadrant_1
    
    def trouver_points_sysmetrie_2e_cadrant(self, list):
        list_point_1er_quadrant = self.trouver_tous_points_1er_cadrant(list)
        list_2nd_quadrant = list_point_1er_quadrant[:]
        for element in list_2nd_quadrant:
            x = (2 * self.x_init) - element[0]
            element[0] = x
        return list_2nd_quadrant
    
    def trouver_points_deuxieme_demi(self, list):
        list_1_quadrant = self.trouver_tous_points_1er_cadrant(list)[:]
        list_2_quadrant = self.trouver_points_sysmetrie_2e_cadrant(list)[:]
        total_1_demi = list_1_quadrant + list_2_quadrant
        total_2_demi = total_1_demi[:]
        for element in total_2_demi:
            y = (2 * self.y_init) - element[1]
            element[1] = y
        return total_2_demi
    
    def trouver_point_tous_cercle_pour_given_z(self, list):
        list_1_quadrant = self.trouver_tous_points_1er_cadrant(list)[:]
        list_2_quadrant = self.trouver_points_sysmetrie_2e_cadrant(list)[:]
        total_1_demi = list_1_quadrant + list_2_quadrant
        total_2_demi = self.trouver_points_deuxieme_demi(list)[:]
        return total_1_demi + total_2_demi
    
    def tous_les_points_ellipsoide(self):
        liste_des_z  = self.trouver_tous_points_z()
        complete_liste = []
        for element in liste_des_z:
            points_cercle = self.trouver_point_tous_cercle_pour_given_z(element)
            complete_liste = complete_liste + points_cercle
        return complete_liste











list_test = [1.694585, 1.694585, 1.694585]
c =  Ellipsoide(1,1,1, 4, 4, 4,100)
print(c.arrete_cube())
print(c.trouver_tous_points_z())
#print(c.trouver_tous_points_1er_cadrant(list_test))
#print(c.trouver_points_deuxieme_demi(list_test))
#print(c.trouver_point_tous_cercle_pour_given_z(list_test))
#print(c.tous_les_points_ellipsoide())
    

        
b = Cone(1,1,1,12,4,8,400)
#print(b.tot_num_cube())
#print(b.volume_1_cube())
#print(b.arrete_cube())
#print(b.find_all_position_of_z())
#print(b.find_pente_entre_rayon())
#print(b.find_rayon_chaque_z())
#print(b.position_all_center_of_circle_r_and_num_cube_in_r())
#print(b.trouver_point_pour_cercle_premier_cadrant(list_test))
#print()
#print(b.find_second_cadrant_left())
#print(b.tot_cericle_at_z(list_test))
#print(b.trouver_tous_les_points_cone())




a = Prisme(1,1,1,4,4,4,64)
#print(a.tot_num_cube())
#print(a.volume_1_cube())
#print(a.arrete_cube())
#print(a.point_milieu_tot())
#print(a.position_milieu_cube_centre())
#print(a.num_cube_largeur_longuer_hauteur_1_cadrant())
#print(a.trouver_point_cube_cadrant_1())
#print(a.trouver_point_cube_cadrant2())
#print(a.create_down_candrants_from_combine_cadrant_1_et_2())
#print(a.complete_list_point_in_prisme())
#print(a.create_liste_cubeinfini_object())
    










        
        





        

        