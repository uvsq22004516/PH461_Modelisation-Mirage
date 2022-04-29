################## Import des librairies ##############################################################
import tkinter as tk

################## Définition des variables globales / constantes : ################################################

menu_principal = tk.Tk()
menu_principal.title("Modélisation de Mirage (PH461)")


################## Définition des variables globales / constantes : ################################################
type_mod = 0 # 1 pour modélisation continue; 2 pour modélisation discrète et explications


def mod_discrete():
    global type_mod
    type_mod = 1
    menu_principal.destroy()
    return type_mod


def mod_continue():
    global type_mod
    type_mod = 2
    menu_principal.destroy()
    return type_mod


############### Définition et placement des widgets : ##############################################################

canvas = tk.Canvas(menu_principal, width = 1200, height = 600, bg = "gray85")
canvas.grid(row=0, rowspan=10, column=0, columnspan=5)

canvas.create_text((600, 200), text="MODÉLISATION D'UN MIRAGE", font=("Rockwell", "20", "bold"))

bouton_mod_continue = tk.Button(menu_principal, text="MODÉLISATION CONTINUE", command=mod_continue, font=("Arial Narrow", "15", "bold italic"), relief="raised", bd=5, bg="gainsboro")
bouton_mod_discrete = tk.Button(menu_principal, text="MODÉLISATION DISCRÈTE", command=mod_discrete, font=("Arial Narrow", "15", "bold italic"), relief="raised", bd=5, bg="gainsboro")

bouton_mod_continue.grid(row=8, column=1)
bouton_mod_discrete.grid(row=8, column=3)
# tk.Entry(menu_principal, cursor="left_ptr")

# insertion image mirage chaud:
img_m_chaud = tk.PhotoImage(file = "m_chaud.png")
label = tk.Label(menu_principal, image=img_m_chaud)
label.grid(row=5, rowspan=3, column=0, columnspan=3)

# insertion image mirage froid:
img_m_froid = tk.PhotoImage(file = "m_froid.png")
label = tk.Label(menu_principal, image=img_m_froid)
label.grid(row=5, rowspan=3, column=3,  columnspan=3)


# canvas.create_line(0, 0, 500, 500, dash = (7,1,1,1))

menu_principal.mainloop()



if type_mod == 1:
    menu_mod_discret = tk.Tk()
    slider = tk.Scale(menu_mod_discret, orient="horizontal", from_= 1, to=25,
      resolution=1, tickinterval=2, length=350,
      label="Nombre de couches")
    slider.grid()
    menu_mod_discret.mainloop()

