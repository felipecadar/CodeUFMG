import sys
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # appropriate import to draw 3d polygons
import pdb

#--- Imprime um triângulo, dados os vértices ------------------------------------
def plotTriangle(points, color='#85BFFF', alpha=0.4):
    srf = Poly3DCollection([points], alpha=alpha, facecolor=color)
    plt.gca().add_collection3d(srf)

#--- Imprime um segmento dados os pontos finais ---------------------------------
def plotLine(p1, p2, color="red", linewidth=2):
    plt.gca().plot([p1[0], p2[0]], [p1[1], p2[1]], zs=[p1[2], p2[2]], color=color, linewidth=linewidth)

#--- Impreme os índices dos três vértices de um triângulo -----------------------
def plotLabel(face, color='black', tamanho=30):
    ax = plt.gca()
    ax.text(vertex[face[0]][0], vertex[face[0]][1], vertex[face[0]][2], "0", color=color, size=tamanho)
    ax.text(vertex[face[1]][0], vertex[face[1]][1], vertex[face[1]][2], "1", color=color, size=tamanho)
    ax.text(vertex[face[2]][0], vertex[face[2]][1], vertex[face[2]][2], "2", color=color, size=tamanho)

def read_ply(path):
    faces = []
    vertex = []
    n_vertex = 0
    n_faces = 0
    with open(path, 'r') as f:
        l = f.readline()
        while 'end_header' not in l:
            if 'element vertex' in l:
                n_vertex = int(l.split(' ')[2].rstrip('\n'))
            if 'element face' in l:
                n_faces = int(l.split(' ')[2].rstrip('\n')) 
            l = f.readline()
        for i in range(n_vertex):
            l = f.readline().rstrip(' \n') #; print(l.split(' ')) ; input()
            vertex.append(list(map(float, l.split(' ')))[:3])
        for i in range(n_faces):
            l = f.readline().rstrip(' \n')
            faces.append(list(map(int, l.split(' ')))[1:4])

    return faces, np.array(vertex)*100

def rotDir(face1_id,face2_id, V):
    face1, face2 = orderPoints(faces[face1_id], faces[face2_id])

    n1 = np.cross( vertex[face1[1]]-vertex[face1[0]] , vertex[face1[2]]-vertex[face1[0]] )
    n2 = np.cross( vertex[face2[1]]-vertex[face2[0]] , vertex[face2[2]]-vertex[face2[0]] )

    if (np.isclose(np.cross(n1,n2),0)).all():
        return(V)

    if np.dot( vertex[face2[0]] - vertex[face1[0]] ,  n1) < 0:
        n1=-n1
    if np.dot( vertex[face1[0]] - vertex[face2[0]] ,  n2) < 0:
        n2=-n2

    K = np.cross(n1,n2)        #--- vetor diretor da reta de interseção dos planos que contém os triângulos
    K = K/np.linalg.norm(K)
   
    cosseno = np.dot(n1,n2)/(np.linalg.norm(n1)*np.linalg.norm(n2))
    seno = np.linalg.norm(np.cross(n1,n2))/(np.linalg.norm(n1)*np.linalg.norm(n2))
    Vrot = cosseno*V + seno*np.cross(K,V) + np.dot(K,V)*(1-cosseno)*K

    return Vrot

def orderPoints(face1, face2):
    s1 = set(face1)
    s2 = set(face2)

    p1 = list((s1 - s2))
    p2 = list((s2 - s1))

    both = list(s1.intersection(s2))

    ordered_face1 = p1 + both
    ordered_face2 = p2 + both[::-1]

    return ordered_face1, ordered_face2

def findPout(face_id,P,V):
    saivertice = -1
    face = faces[face_id]
    reordered_face = []

    # Loop para achar o lado do ponto P no triangulo 
    for i,j,k in [[face[0], face[1], face[2]], [face[1], face[2], face[0]], [face[2], face[0], face[1]]]:

        if not np.isclose(np.cross(vertex[i] - P, vertex[j] - P), 0).all():
            continue

        # O ponto P esta no lado i->j
        # Verifica se o ponto de saida esta no ponto k do trinagulo (problematico...)
        if (np.isclose((np.cross(vertex[k]-P,V)),0)).all():
            Pout = vertex[k]
            saivertice = k
        else:
            # Consistencia entre triangulos! Obriga o ponto Pout estar no lado j->k
            if np.dot(np.cross(V,vertex[i]-P),np.cross(V,vertex[k]-P)) < 0:
                i , j = j , i 

            nabc = np.cross( vertex[j] - vertex[i] , vertex[k] - vertex[i] )
            nnbc = np.cross(nabc, vertex[k] - vertex[j])
            r = np.dot(vertex[j] - P , nnbc)/np.dot(V,nnbc)
            Pout = P + r*V

        return Pout, [k, j], saivertice
    
def findFace(poits, exclude=[]):
    for i in range(len(faces)):
        p1, p2 = poits
        if not (i in exclude):
            if p1 in faces[i] and p2 in faces[i]:
                return i
    return None

def randColor():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="", required=False, 
                        help="Input mesh to run geodesic walk")
    parser.add_argument('-p', '--plot_mesh', action='store_true')
    parser.add_argument('-m', '--max-seg', type=int, help="Max number of segments to walk", default=50)
    return parser.parse_args()


plt.figure(figsize=(8,8))
ax=plt.subplot(111,projection='3d')

args = parseArgs()

plot_mesh = args.plot_mesh
input_mesh = args.input

if input_mesh == '':
    vertex = [
        np.array([0,0,0]),
        np.array([1,0,0]),
        np.array([0,1,0]),
        np.array([1,1,1]),
    ]

    faces = [
        [0, 1, 2],
        [1, 2, 3],
    ]

    nte=0
    P1 = 1
    V = 1*(vertex[faces[nte][1]] - vertex[faces[nte][0]]) + 2*(vertex[faces[nte][2]] - vertex[faces[nte][0]])

else:
    faces, vertex = read_ply(args.input)

    nte=30
    P1 = 1
    V = 1*(vertex[faces[nte][1]] - vertex[faces[nte][0]]) + 1*(vertex[faces[nte][2]] - vertex[faces[nte][0]])

face_now = nte
P_now = vertex[faces[nte][0]]
V_now = V

max_path = args.max_seg
path = []

for i in range(max_path):

    # Find intersect
    intersect, out_side, out_vert  = findPout(face_now, P_now, V_now)
    if out_vert > -1 :
        print("Out in Vertex {}".format(out_vert))
        break

    path.append([face_now, P_now, intersect])

    # Find next face
    next_face = findFace(out_side, [face_now])
    if next_face == None:
        print("Missing next face")
        break
    
    # Rotate Vector
    V_now = rotDir(face_now, next_face, V_now)
    
    face_now = next_face
    P_now = intersect


# plots
if plot_mesh:
    for f in faces:
        plotTriangle((vertex[f[0]], vertex[f[1]], vertex[f[2]]), color=randColor())

used_vertex = []
for p in path:
    face_now, P_now, intersect = p

    used_vertex.append((vertex[faces[face_now][0]]))
    used_vertex.append((vertex[faces[face_now][1]]))
    used_vertex.append((vertex[faces[face_now][2]]))

    plotLine(P_now, intersect)
    plt.plot([P_now[0]], [P_now[1]], [P_now[2]], marker="o", color="red", markersize=2)
    plt.plot([intersect[0]], [intersect[1]], [intersect[2]], marker="o", color="red")
    plotTriangle((vertex[faces[face_now][0]], vertex[faces[face_now][1]], vertex[faces[face_now][2]]), color=randColor(), alpha=0.4)

if plot_mesh:
    mins = np.min(np.array(vertex), axis=0)
    maxs = np.max(np.array(vertex), axis=0)
else:
    mins = np.min(np.array(used_vertex), axis=0)
    maxs = np.max(np.array(used_vertex), axis=0)

ax.set_xlim(mins[0],maxs[0])
ax.set_ylim(mins[1],maxs[1])
ax.set_zlim(mins[2],maxs[2])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()