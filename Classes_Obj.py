#kg par m^3
#1 mini = 1kg
#all mass in kg
#all coord in meters
import math
PI = math.pi

class CubeInfini:
    #Create a point with a mass and position
    def __init__(self, position_x, position_y, position_z, volume, masse):
        self.volume_cube = volume
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.masse = masse
    #To take back position of the point
    def position(self):
        return [self.position_x, self.position_y, self.position_z]
    def mass(self):
        return self.masse
    def volume(self):
        return self.volume_cube
    
    

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


    def vrai_mass(self):
        num_points = len(self.complete_list_point_in_prisme())
        mass = self.masse
        vrai_mass_cube = mass / num_points
        return vrai_mass_cube


    def create_liste_cubeinfini_object(self):
        points = self.complete_list_point_in_prisme()[:]
        list_obj = []
        for positions in points:
            a = CubeInfini(positions[0], positions[1], positions[2], self.volume_1_cube(), self.vrai_mass())
            list_obj.append(a)
        return list_obj







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
        return (self.volume_1_cube() ** (1/3))
    
    def find_all_position_of_z(self):
        starting_z = (self.arrete_cube() / 2) + self.z_center
        number_cube_en_z = 0
        list_z = []
        while starting_z <= (self.hauteur) + self.z_center:
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
                rayon = (z - (self.hauteur + self.z_center))/pente
                rayon += rayon_haut
            elif pente > 0:
                rayon = (z - self.z_center)/pente
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
        while (y - self.y_center)**2 <= (rayon ** 2) - ((x - self.x_center) ** 2):
            while (x - self.x_center)**2 <= (rayon ** 2) - ((y - self.y_center) ** 2):
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
    
    def vrai_mass(self):
        num_points = len(self.trouver_tous_les_points_cone())
        mass = self.masse
        vrai_mass_cube = mass / num_points
        return vrai_mass_cube
    
    def create_liste_cubeinfini_object(self):
        points = self.trouver_tous_les_points_cone()[:]
        list_obj = []
        for positions in points:
            a = CubeInfini(positions[0], positions[1], positions[2], self.volume_1_cube(), self.vrai_mass())
            list_obj.append(a)
        return list_obj









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
        return self.volume_1_cube() ** (1/3)
    
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
        max = self.rayon_Z + self.z_init
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
    
    def vrai_mass(self):
        num_points = len(self.tous_les_points_ellipsoide())
        mass = self.masse
        vrai_mass_cube = mass / num_points
        return vrai_mass_cube
    
    def create_liste_cubeinfini_object(self):
        points = self.tous_les_points_ellipsoide()[:]
        list_obj = []
        for positions in points:
            a = CubeInfini(positions[0], positions[1], positions[2], self.volume_1_cube(), self.vrai_mass())
            list_obj.append(a)
        return list_obj


CONSTANT = 0.01
GRAVITE = 9.81

class VectorCreation:
    def __init__(self, list_1_object, list_2_object):
        self.list_1 = list_1_object
        self.list_2 = list_2_object
    
    def distance_2_object(self, object_1_depart, object_2):
        list_position_1_depart = object_1_depart.position()
        list_position_2 = object_2.position()
        x_1_d = list_position_1_depart[0]
        x_2 = list_position_2[0]
        y_1_d = list_position_1_depart[1]
        y_2 = list_position_2[1]
        z_1_d = list_position_1_depart[2]
        z_2 = list_position_2[2]
        distance = (((x_2 - x_1_d) ** 2) + ((y_2 - y_1_d) ** 2) + ((z_2 - z_1_d) ** 2)) ** (1/2)
        return distance

    def trouver_vecteur_unitaire_entre_2_objects(self, object_1_depart, object_2):
        list_position_1_depart = object_1_depart.position()
        list_position_2 = object_2.position()
        x_1_d = list_position_1_depart[0]
        x_2 = list_position_2[0]
        y_1_d = list_position_1_depart[1]
        y_2 = list_position_2[1]
        z_1_d = list_position_1_depart[2]
        z_2 = list_position_2[2]
        distance = (((x_2 - x_1_d) ** 2) + ((y_2 - y_1_d) ** 2) + ((z_2 - z_1_d) ** 2)) ** (1/2)
        vecteur_unitaire = [((x_2 - x_1_d)/distance),((y_2 - y_1_d)/distance),((z_2 - z_1_d)/distance)]
        return vecteur_unitaire
    
    def trouver_force_2_masse(self, object_1, object_2):
        masse_1 = object_1.mass()
        masse_2 = object_2.mass()
        distance = self.distance_2_object(object_1, object_2)
        force = GRAVITE * masse_1 * masse_2 / (distance ** 2)
        return force

    def tout_vecteur_a_1_point(self, object_1, list_other_all_object):
        tot_vecteur = [0,0,0]
        for object_from_tot_object in list_other_all_object:
            vecteur_unitaire_de_object_1 = self.trouver_vecteur_unitaire_entre_2_objects(object_1, object_from_tot_object)[:]
            magnetude_force = self.trouver_force_2_masse(object_1, object_from_tot_object)
            vecteur_1_froce = []
            for element in vecteur_unitaire_de_object_1:
                composante_vecteur_de_force_mini = element * magnetude_force
                vecteur_1_froce.append(composante_vecteur_de_force_mini)
            tot_vecteur[0] += vecteur_1_froce[0]
            tot_vecteur[1] += vecteur_1_froce[1]
            tot_vecteur[2] += vecteur_1_froce[2]
        return tot_vecteur
    
    def trouver_vecteur_force_tout_point_1_object_venant_autre(self, list_object_a_etudier, list_object_2):
        liste_out = []
        for object_a_etudier in list_object_a_etudier:
            vecteur_force_appliquer_au_point = self.tout_vecteur_a_1_point(object_a_etudier, list_object_2)
            position_obj = object_a_etudier.position()
            liste_a_lire_output = [position_obj, vecteur_force_appliquer_au_point]
            liste_out.append(liste_a_lire_output)
        return liste_out
    
    def retour_listes_position_vecter(self):
        list_obj_1 = self.list_1
        list_obj_2 = self.list_2
        liste_complete_obj_1 = self.trouver_vecteur_force_tout_point_1_object_venant_autre(list_obj_1, list_obj_2)
        liste_complete_obj_2 = self.trouver_vecteur_force_tout_point_1_object_venant_autre(list_obj_2, list_obj_1)
        return (liste_complete_obj_1, liste_complete_obj_2)

        



    









c =  Ellipsoide(10,10,10, 4, 4, 4,100)
#print(c.arrete_cube())
#print(c.trouver_tous_points_z())
#print(c.trouver_tous_points_1er_cadrant(list_test))
#print(c.trouver_points_deuxieme_demi(list_test))
#print(c.trouver_point_tous_cercle_pour_given_z(list_test))
#print(c.tous_les_points_ellipsoide())
print(len(c.create_liste_cubeinfini_object()))
list_1 = c.create_liste_cubeinfini_object()
print(len(list_1))
    

        
b = Cone(100,100,100,2,4,8,400)
#print(b.tot_num_cube())
#print(b.volume_1_cube())
#print(b.arrete_cube())
#print(b.find_all_position_of_z())
#print(b.find_pente_entre_rayon())
#print(b.find_rayon_chaque_z())
##print(b.position_all_center_of_circle_r_and_num_cube_in_r())
#print(b.trouver_point_pour_cercle_premier_cadrant(list_test))
#print()
#print(b.find_second_cadrant_left())
#print(b.tot_cericle_at_z(list_test))
print(len(b.trouver_tous_les_points_cone()))
#print((b.create_liste_cubeinfini_object()))

#print(b.trouver_tous_les_points_cone())
list_2 = b.create_liste_cubeinfini_object()




a = Prisme(0,0,1110,4,4,4,640)
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
print(len(a.create_liste_cubeinfini_object()))
#print(len(a.create_liste_cubeinfini_object()))



test = VectorCreation(list_1, list_2)
print(test.retour_listes_position_vecter())



        



        

        