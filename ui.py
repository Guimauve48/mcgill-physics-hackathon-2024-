import pygame 
import math
  
pygame.init() 

windowWidth = 1500
windowHeight = 800

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("McGill Physics Hackathon 2024") 

colors = {"black":(0,0,0), "white":(255,255,255), "lgray": (211,211,211), "gray": (175,175,175), 
          "lblue":(173,216,230), "hblue":(120,195,215), "red":(220,20,60), "blue":(0,0,205), "green":(50,205,50)}
centerPos = ((windowWidth*5/6)/2 + windowWidth/6, windowHeight/2)
theta = math.atan(math.cos(math.pi/4))
beta = math.atan(2/3)
alpha = theta - beta
gamma = math.pi/2 -theta - beta
phi = math.atan(1/2)
epsilon = theta - phi
tau = math.pi/2 -theta - phi
PI = math.pi
P = 1.1

def to2d(x,y,z, main):
    center = centerPos if not main else (0,0)
    return (center[0]+y-x*math.cos(theta), center[1]+z+x*math.sin(theta))

def moveX(pos, x):
    return (pos[0]+x/2*math.cos(theta), pos[1]-x/2*math.sin(theta))

def ellipse(rY, rZ, c, x):
    delta = ((1-((x-c[0])**2)/rY) * rZ)**0.5
    return (c[1] - delta, c[1] + delta)

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

#? Prism class
class Prism:
    def __init__(self, position, size, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.sizeZ = size[2]
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]

        self.create()

    def create(self):
        p4 = to2d(self.x, self.y, self.z, self.main)
        p1 = moveX(p4,-self.sizeX)
        p0 = (p1[0], p1[1]+self.sizeZ)
        p2 = (p1[0]+self.sizeY, p1[1])
        p3 = (p0[0]+self.sizeY, p0[1])
        p5 = moveX(p2,self.sizeX)
        p6 = moveX(p3,self.sizeX)
        self.points = [p0,p1,p2,p3,p4,p5,p6]
        self.corners = (p0,p5)
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face1 = (*p1, self.sizeY, self.sizeZ)
        self.face2 = (p1, p4, p5, p2)
        self.face3 = (p2, p5, p6, p3)

    def draw(self):
        self.create()
        pygame.draw.rect(window, self.color, self.face1)
        pygame.draw.polygon(window, self.color, self.face2)
        pygame.draw.polygon(window, self.color, self.face3)
        pygame.draw.lines(window, colors["black"], False, [self.points[3],self.points[0],self.points[1],self.points[2],self.points[3],self.points[6],self.points[5],self.points[4],self.points[1]])
        pygame.draw.line(window, colors["black"],self.points[2],self.points[5])

    def volume_tot(self):
        return (self.sizeX * self.sizeY * self.sizeZ)
    
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
        point_2 = [self.x + self.sizeX, self.y, self.z]
        point_3 = [self.x, self.y + self.sizeY, self.z]
        point_4 = [self.x + self.sizeX, self.y + self.sizeY, self.z]
        list_points_plan_base = [point_1, point_2, point_3, point_4]
        return list_points_plan_base
    
    def point_milieu_tot(self):
        point_milieu = [(self.x + (self.sizeX / 2)), (self.y + (self.sizeY / 2)), (self.z + (self.sizeZ / 2))]
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

        while (position) <= (self.sizeX / 2):
            position += self.arrete_cube()
            num_cube_largeur += 1

        position = (self.arrete_cube() / 2)

        while (position) <= (self.sizeX / 2):
            position += self.arrete_cube()
            num_cube_longueur += 1
        
        position = (self.arrete_cube() / 2)
        while (position) <= (self.sizeX / 2):
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
        transverser = (self.sizeX) / 2
        for point in list_point_cadrant_2:
            point[0] = point[0] - transverser

        return list_point_cadrant_2
    
    def create_down_candrants_from_combine_cadrant_1_et_2(self):
        list_cadran_1 = self.trouver_point_cube_cadrant_1()[:]
        list_cadran_2 = self.trouver_point_cube_cadrant2()[:]
        list_quart_forme = list_cadran_1 + list_cadran_2
        transverser = (self.sizeX) / 2

        for element in list_quart_forme:
            element[2] = element[2] - transverser
        return list_quart_forme
    
    def create_total_points_for_prisme(self):
        down_qurater = self.create_down_candrants_from_combine_cadrant_1_et_2()[:]
        up_quarter = self.trouver_point_cube_cadrant_1()[:] + self.trouver_point_cube_cadrant2()[:]
        half_solid = down_qurater + up_quarter
        transverser = (self.sizeX) / 2
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


#? Cylinder class
class Cylinder:
    def __init__(self, position, r1, r2, height, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.r1 = r1
        self.r2 = r2
        self.height = height
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]
        
        self.create()


    def create(self):
        self.center = to2d(self.x, self.y, self.z, self.main)
        self.corners = ((self.center[0]-max(self.r1,self.r2)*P, self.center[1]+self.height*P+max(self.r1,self.r2)*P/2),(self.center[0]+max(self.r1,self.r2)*P, self.center[1]-max(self.r1,self.r2)*P/2))
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face1 = ((self.center[0]-self.r1*P,self.center[1]),
                      (self.center[0]-self.r2*P,self.center[1]+self.height*P),
                      (self.center[0]+self.r2*P,self.center[1]+self.height*P),
                      (self.center[0]+self.r1*P,self.center[1]))
        self.top = (self.center[0]-self.r1*P, self.center[1]-self.r1*P/2, self.r1*2*P, self.r1*P)
        self.bottom = (self.center[0]-self.r2*P, self.center[1]+self.height*P-self.r2*P/2, self.r2*2*P, self.r2*P)

    def draw(self):
        self.create()

        pygame.draw.ellipse(window, self.color, self.bottom)
        pygame.draw.ellipse(window, colors["black"], self.bottom,1)

        pygame.draw.polygon(window, self.color, self.face1)

        pygame.draw.ellipse(window, self.color, self.top)
        pygame.draw.ellipse(window, colors["black"], self.top,1)

        pygame.draw.line(window, colors["black"],(self.center[0]-self.r1*P,self.center[1]),(self.center[0]-self.r2*P,self.center[1]+self.height*P))
        pygame.draw.line(window, colors["black"],(self.center[0]+self.r1*P,self.center[1]),(self.center[0]+self.r2*P,self.center[1]+self.height*P))

    def volume_tot(self):
        return round((PI/3) * (self.height) * ((self.r1 ** 2) + (self.r2 ** 2) + (self.r1 * self.r2)))
    
    def tot_num_cube(self):
        return self.masse
    
    def volume_1_cube(self):
        return self.volume_tot() / self.tot_num_cube()
    
    def arrete_cube(self):
        return (self.volume_1_cube() ** (1/3))
    
    def find_all_position_of_z(self):
        starting_z = (self.arrete_cube() / 2) + self.z
        number_cube_en_z = 0
        list_z = []
        while starting_z <= (self.height) + self.z:
            list_z.append(starting_z)
            starting_z += self.arrete_cube()
            number_cube_en_z += 1
        return list_z


    def find_pente_entre_rayon(self):
        r2 = self.r2
        r1 = self.r1
        if r2 == r1:
            return 0
        y_1 = self.height
        y_2 = 0
        x_1 = 0
        x_2 = (r1 - r2)
        pente_droite_entre_rayon = (y_1 - y_2) / (x_1 - x_2)
        return pente_droite_entre_rayon
    
    def find_rayon_chaque_z(self):
        list_des_z = self.find_all_position_of_z()[:]
        r2 = self.r2
        r1 = self.r1
        pente = self.find_pente_entre_rayon()
        liste_z_with_r = []
        for z2 in list_des_z:
            if pente == 0:
                rayon = r1
            elif pente < 0:
                rayon = (z2 - (self.height + self.z))/pente
                rayon += r2
            elif pente > 0:
                rayon = (z2 - self.z)/pente
                rayon += r1
            liste_z_with_r.append([z2, rayon])
        return liste_z_with_r
    
    def position_first_cube_per_innercircle(self):
        position_x = self.x + (self.arrete_cube() / 2)
        position_y = self.y + (self.arrete_cube() / 2)
        return [position_x, position_y]
    
    def position_all_center_of_circle_r_and_num_cube_in_r(self):
        list_des_z = self.find_rayon_chaque_z()[:]
        liste_complete = []
        for z2 in list_des_z:
            rayon = z2[1]
            if (self.arrete_cube() / 2) > rayon:
                num_cube = 0
            else: 
                num_cube = (rayon + (self.arrete_cube() / 2))//(self.arrete_cube())
            position_x_y = self.position_first_cube_per_innercircle()[:]
            liste_a_append = position_x_y + z2 + [num_cube]
            liste_complete.append(liste_a_append)
        return liste_complete
    
    

    def trouver_point_pour_cercle_premier_cadrant(self, list_info):
        x2 = list_info[0]
        y2 = list_info[1]
        z2 = list_info[2]
        rayon = list_info[3]
        list_cadrant_1 = []
        while (y2 - self.y)**2 <= (rayon ** 2) - ((x2 - self.x) ** 2):
            while (x2 - self.x)**2 <= (rayon ** 2) - ((y2 - self.y) ** 2):
                list_adding = [x2,y2] + [z2]
                list_cadrant_1.append(list_adding)
                x2 += (self.arrete_cube())
            x2 = list_info[0]
            y2 += (self.arrete_cube())
        return list_cadrant_1
    
    list_test = [1.816675, 1.816675, 0.816675, 11.183325, 7.0]
    def find_second_cadrant_left(self, list):
        point_1_cadrant = self.trouver_point_pour_cercle_premier_cadrant(list)
        point_2e_cadrant = point_1_cadrant[:]
        for element in point_2e_cadrant:
            x2 = (2 * self.x) - element[0]
            element[0] = x2
        return point_2e_cadrant
    
    def demi_cercle(self, list):
        quarter_1 = self.trouver_point_pour_cercle_premier_cadrant(list)
        quarter_2 = self.find_second_cadrant_left(list)
        return quarter_1 + quarter_2


    def other_half_circle(self, list):
        demi_cercle = self.demi_cercle(list)
        demi_cercle_a_return = demi_cercle[:]
        for element in demi_cercle_a_return:
            y2 = (2 * self.y) - element[1]
            element[1] = y2
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
    

#? Ellipsoid class
class Ellipsoid:
    def __init__(self, position, rX, rY, rZ, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.rX = rX
        self.rY = rY
        self.rZ = rZ
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]

        self.create()


    def create(self):
        self.center = to2d(self.x, self.y, self.z, self.main)
        self.corners = ((self.center[0]-self.rY*P, self.center[1]+self.rZ*P),(self.center[0]+self.rY*P, self.center[1]-self.rZ*P))
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face = (self.center[0]-self.rY*P, self.center[1]-self.rZ*P, self.rY*2*P, self.rZ*2*P)


    def draw(self):
        self.create()

        pygame.draw.ellipse(window, self.color, self.face)
        pygame.draw.ellipse(window, colors["black"], self.face,1)

        #for (i,arc) in enumerate(self.arcs):
        #    print(i,arc)
        #    pygame.draw.arc(window, colors["black"], arc, math.pi*2/3, math.pi*4/3)


    def volume_tot(self):
        return (4/3) * (PI) * (self.rX * self.rY * self.rZ)
    
    def tot_num_cube(self):
        return self.masse
    
    def volume_1_cube(self):
        return self.volume_tot() / self.tot_num_cube()
    
    def arrete_cube(self):
        return self.volume_1_cube() ** (1/3)
    
    def point_milieu_cube(self):
        x_intitial = self.x + (self.arrete_cube() / 2)
        y_intitial = self.y + (self.arrete_cube() / 2)
        z_intitial = self.z + (self.arrete_cube() / 2)
        return [x_intitial, y_intitial, z_intitial]

    def trouver_tous_points_z(self):
        point_ini = self.point_milieu_cube() 
        x_test = point_ini[0]
        y_test = point_ini[1]
        z_test = point_ini[2]
        max = self.rZ + self.z
        list_point_milieu = []
        while z_test <= max:
            list_point_milieu.append([x_test, y_test, z_test])
            z_test += self.arrete_cube()
        return list_point_milieu

    def trouver_tous_points_1er_cadrant(self, list):
        position_x = list[0]
        position_y = list[1]
        position_z = list[2]
        x = self.x
        y = self.y
        list_cadrant_1 = []
        while (position_y - y) **2 <= ((self.rY) ** 2) * (1 - (((position_x - x) ** 2) / ((self.rX) ** 2))):
            while (position_x - x) **2 <= ((self.rY) ** 2) * (1 - (((position_y - y) ** 2) / ((self.rX) ** 2))):
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
            x = (2 * self.x) - element[0]
            element[0] = x
        return list_2nd_quadrant
    
    def trouver_points_deuxieme_demi(self, list):
        list_1_quadrant = self.trouver_tous_points_1er_cadrant(list)[:]
        list_2_quadrant = self.trouver_points_sysmetrie_2e_cadrant(list)[:]
        total_1_demi = list_1_quadrant + list_2_quadrant
        total_2_demi = total_1_demi[:]
        for element in total_2_demi:
            y = (2 * self.y) - element[1]
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

        

#! Object selection section
section_bg = pygame.rect.Rect(0,0, windowWidth/6, windowHeight)

mainPrism = Prism((0,windowWidth/12-20,windowHeight*1/6-25), (80,80,80), True, 100)
mainCylinder = Cylinder((0,windowWidth/12,windowHeight/2-40), 50,50,80, True, 100)
mainEllipsoid = Ellipsoid((0,windowWidth/12,windowHeight*5/6-20), 40,80,50, True, 100)

xGrab, yGrab, zGrab = False, False, False

shapeList = []
pointsList = []
selectedShape = None

running = True  
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            xGrab, yGrab, zGrab = False, False, False

            pointsList = [shape.create_liste_cubeinfini_object() for shape in shapeList]
            if len(pointsList) == 2:
                vectors = VectorCreation(*pointsList)



        if selectedShape != None:
            c = selectedShape.arrowC
            cX = moveX(c, -180)
            cY = (c[0]+100, c[1])
            cZ = (c[0], c[1]-100)
            
            if (pygame.mouse.get_pos()[0] >= c[0] and pygame.mouse.get_pos()[0] <= cY[0] and
                pygame.mouse.get_pos()[1] >= c[1] - 10 and pygame.mouse.get_pos()[1] <= c[1] + 10):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    diff = pygame.mouse.get_pos()[0] - selectedShape.y
                    yGrab = True
            
            elif (pygame.mouse.get_pos()[0] >= c[0] - 10 and pygame.mouse.get_pos()[0] <= c[0] + 10 and
                pygame.mouse.get_pos()[1] >= cZ[1] and pygame.mouse.get_pos()[1] <= c[1]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    diff = pygame.mouse.get_pos()[1] - selectedShape.z
                    zGrab = True
            
            elif (pygame.mouse.get_pos()[0] >= cX[0] and pygame.mouse.get_pos()[0] <= c[0] and
                  pygame.mouse.get_pos()[1] <= cX[1] and pygame.mouse.get_pos()[1] >= c[1]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    lastVal = pygame.mouse.get_pos()
                    xGrab = True
                
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    found = False
                    for shape in shapeList[::-1]:
                        if not found:
                            if (pygame.mouse.get_pos()[0] >= shape.corners[0][0] and pygame.mouse.get_pos()[0] <= shape.corners[1][0] and
                                pygame.mouse.get_pos()[1] >= shape.corners[1][1] and pygame.mouse.get_pos()[1] <= shape.corners[0][1]):
                                
                                if selectedShape != None:
                                        selectedShape.color = colors["lblue"]

                                if shape == selectedShape:
                                    selectedShape = None
                                else:
                                    selectedShape = shape
                                    selectedShape.color = colors["hblue"]

                                found = True
                            else:
                                if selectedShape != None:
                                        selectedShape.color = colors["lblue"]
                                selectedShape = None

        elif (pygame.mouse.get_pos()[0] >= mainPrism.corners[0][0] and pygame.mouse.get_pos()[0] <= mainPrism.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainPrism.corners[1][1] and pygame.mouse.get_pos()[1] <= mainPrism.corners[0][1]):
            mainPrism.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Prism((0,0,0), (100,100,100), False, 100))

        elif (pygame.mouse.get_pos()[0] >= mainCylinder.corners[0][0] and pygame.mouse.get_pos()[0] <= mainCylinder.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainCylinder.corners[1][1] and pygame.mouse.get_pos()[1] <= mainCylinder.corners[0][1]):
            mainCylinder.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Cylinder((0,0,0), 10, 40, 80, False, 100))

        elif (pygame.mouse.get_pos()[0] >= mainEllipsoid.corners[0][0] and pygame.mouse.get_pos()[0] <= mainEllipsoid.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainEllipsoid.corners[1][1] and pygame.mouse.get_pos()[1] <= mainEllipsoid.corners[0][1]):
            mainEllipsoid.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Ellipsoid((0,0,0), 40, 80, 50, False, 100))
        
        else:
            mainPrism.color = colors["lblue"]
            mainEllipsoid.color = colors["lblue"]
            mainCylinder.color = colors["lblue"]
            mainEllipsoid.color = colors["lblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.MOUSEBUTTONDOWN:
                found = False
                for shape in shapeList[::-1]:
                    if not found:
                        if (pygame.mouse.get_pos()[0] >= shape.corners[0][0] and pygame.mouse.get_pos()[0] <= shape.corners[1][0] and
                            pygame.mouse.get_pos()[1] >= shape.corners[1][1] and pygame.mouse.get_pos()[1] <= shape.corners[0][1]):
                            if selectedShape != None:
                                    selectedShape.color = colors["lblue"]

                            if shape == selectedShape:
                                selectedShape = None
                            else:
                                selectedShape = shape
                                selectedShape.color = colors["hblue"]

                            found = True    


    window.fill(colors["white"])

    #! Movement
    if selectedShape != None:
        if xGrab:
            mouseNow = pygame.mouse.get_pos()
            yChange = mouseNow[0] - lastVal[0]
            zChange = mouseNow[1] - lastVal[1]

            sign = -1 if yChange > 0 and zChange < 0 else 1
            changeX = (yChange**2 + zChange**2)**0.5 * sign

            selectedShape.x += changeX
            lastVal = pygame.mouse.get_pos()
        if yGrab:
            selectedShape.y = pygame.mouse.get_pos()[0] - diff
        if zGrab:
            selectedShape.z = pygame.mouse.get_pos()[1] - diff


    #! Axis
    pygame.draw.line(window, colors["gray"], (centerPos[0]-windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3, centerPos[1]))
    pygame.draw.aaline(window, colors["gray"], (centerPos[0]+windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3-15, centerPos[1]+10),2)
    pygame.draw.aaline(window, colors["gray"], (centerPos[0]+windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3-15, centerPos[1]-10),2)

    pygame.draw.line(window, colors["gray"], (centerPos[0], centerPos[1]+windowHeight*3/7),(centerPos[0], centerPos[1]-windowHeight*3/7))
    pygame.draw.aaline(window, colors["gray"], (centerPos[0], centerPos[1]-windowHeight*3/7),(centerPos[0]-10, centerPos[1]-windowHeight*3/7+15),2)
    pygame.draw.aaline(window, colors["gray"], (centerPos[0], centerPos[1]-windowHeight*3/7),(centerPos[0]+10, centerPos[1]-windowHeight*3/7+15),2)
    
    pygame.draw.line(window, colors["gray"], moveX(centerPos,windowWidth*4/7),moveX(centerPos,-windowWidth*4/7))
    pt = moveX(centerPos,-windowWidth*4/7)
    pygame.draw.line(window, colors["gray"], pt, (pt[0]+(325**0.5)*math.cos(alpha), pt[1]+(325**0.5)*math.sin(alpha)))
    pygame.draw.line(window, colors["gray"], pt, (pt[0]+(325**0.5)*math.sin(gamma), pt[1]-(325**0.5)*math.cos(gamma)))

    
    #! Main shapes
    pygame.draw.rect(window, colors["lgray"], section_bg)
    mainPrism.draw()
    mainCylinder.draw()
    mainEllipsoid.draw()

    #! Added shapes
    for shape in shapeList:
        shape.draw()

    #! Selected shape arrows
    if selectedShape != None:
        c = selectedShape.arrowC
        cX = moveX(c, -180)
        cY = (c[0]+100, c[1])
        cZ = (c[0], c[1]-100)

        pygame.draw.line(window, colors["blue"], moveX(c, -8), cX, 4)
        pygame.draw.circle(window, colors["blue"], moveX(moveX(c, -8)[::-1],2)[::-1], 2)
        pygame.draw.polygon(window, colors["blue"], (moveX(cX,-24), moveX((cX[0]+(180**0.5)*math.cos(epsilon), cX[1]+(180**0.5)*math.sin(epsilon-0.1)),-24),moveX((cX[0]+(180**0.5)*math.sin(tau), cX[1]-(180**0.5)*math.cos(tau)),-24)))

        pygame.draw.line(window, colors["red"], (c[0], c[1]-8), cZ, 4)
        pygame.draw.circle(window, colors["red"], (c[0]+1, c[1]-8), 2)
        pygame.draw.polygon(window, colors["red"], ((cZ[0], cZ[1]-12), (cZ[0]-6, cZ[1]), (cZ[0]+6, cZ[1])))

        pygame.draw.line(window, colors["green"], (c[0]+8, c[1]), cY, 4)
        pygame.draw.circle(window, colors["green"], (c[0]+8, c[1]+1), 2)
        pygame.draw.polygon(window, colors["green"], ((cY[0]+12, cY[1]), (cY[0], cY[1]-6), (cY[0], cY[1]+6)))


    if len(pointsList) == 2:
        vectors = VectorCreation(*pointsList).retour_listes_position_vecter()
        for sh in vectors:
            for (pos, vec) in sh:
                p0 = to2d(pos[0],pos[1],pos[2], False)
                p1 = to2d(pos[0]+vec[0]*100,pos[1]+vec[1]*100,pos[2]+vec[2]*100, False)

                pygame.draw.line(window, colors["red"], p0, p1)

    pygame.display.update() 

pygame.quit()
