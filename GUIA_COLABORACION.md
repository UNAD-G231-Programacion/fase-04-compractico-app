# 🤝 Guía de Colaboración — Flujo de Trabajo con Git y GitHub

> **Regla principal:** Nadie trabaja directamente sobre `main`. Cada integrante del equipo debe crear y trabajar en su propia rama.

---

## 📋 Requisitos previos

- Tener **Git** instalado en tu equipo
- Tener una cuenta en **GitHub**
- Haber sido agregado como colaborador al repositorio

---

## 🚀 Paso 1 — Clonar el repositorio

Copia el enlace del repositorio desde GitHub y ejecuta en tu terminal:

```bash
git clone https://github.com/usuario/nombre-del-repositorio.git
```

Luego entra a la carpeta del proyecto:

```bash
cd nombre-del-repositorio
```

> ⚠️ **Importante:** Al clonar un repositorio, Git ya está inicializado automáticamente. **No ejecutes** `git init`, ya que podría causar conflictos.

---

## 🌿 Paso 2 — Crear tu rama de trabajo

Antes de crear tu rama, asegúrate de estar en `main` y tener la versión más reciente:

```bash
git checkout main
git pull origin main
```

Ahora crea tu rama personal con el siguiente formato:

```
feature-nombre-del-estudiante
```

**Ejemplo:**

```bash
git checkout -b feature-juan-perez
```

> Este comando crea la rama **y** te mueve a ella automáticamente.

---

## 💻 Paso 3 — Trabajar en tu rama

A partir de este momento, todos tus cambios deben realizarse estando en **tu rama**. Puedes verificar en qué rama estás con:

```bash
git branch
```

La rama activa aparecerá marcada con un asterisco `*`.

---

## 💾 Paso 4 — Guardar cambios (commits)

Cada vez que avances en tu trabajo, guarda los cambios con los siguientes comandos:

**1. Ver qué archivos modificaste:**
```bash
git status
```

**2. Agregar los archivos al área de preparación:**
```bash
# Agregar todos los archivos modificados
git add .

# O agregar un archivo específico
git add nombre-del-archivo.ext
```

**3. Crear el commit con un mensaje descriptivo:**
```bash
git commit -m "Descripción breve de lo que hiciste"
```

> ✅ **Buenas prácticas para el mensaje del commit:**
> - Sé claro y específico: `"Agrega formulario de registro de usuario"`
> - Evita mensajes vagos como: `"cambios"` o `"actualización"`

---

## ☁️ Paso 5 — Subir tu rama a GitHub

La primera vez que subas tu rama, usa:

```bash
git push -u origin feature-nombre-del-estudiante
```

> El flag `-u` vincula tu rama local con la remota. A partir de ahí, cada vez que quieras subir nuevos commits, simplemente ejecuta:

```bash
git push
```

---

## 🔁 Paso 6 — Mantener tu rama actualizada

Si otros compañeros han hecho cambios en `main`, es importante que actualices tu rama para evitar conflictos:

```bash
git checkout main
git pull origin main
git checkout feature-nombre-del-estudiante
git merge main
```

---

## 📬 Paso 7 — Crear un Pull Request (PR) hacia main

Cuando hayas terminado tu trabajo y quieras integrarlo al proyecto:

1. Asegúrate de haber subido todos tus commits a GitHub (`git push`)
2. Ve al repositorio en **GitHub**
3. Haz clic en el botón **"Compare & pull request"** que aparece al detectar tu rama
4. Agrega un **título claro** y una **descripción** de los cambios realizados
5. Haz clic en **"Create pull request"**

> 🔒 Un compañero o el responsable del proyecto revisará los cambios antes de aprobarlos y hacer el merge hacia `main`.

---

## 🗺️ Resumen del flujo

```
Clonar repo → Crear rama feature-tu-nombre → Trabajar y hacer commits
     → git push → Crear Pull Request → Revisión → Merge a main
```

---

## ❓ Comandos de referencia rápida

| Acción | Comando |
|---|---|
| Ver ramas existentes | `git branch` |
| Cambiar de rama | `git checkout nombre-rama` |
| Ver estado de archivos | `git status` |
| Ver historial de commits | `git log --oneline` |
| Traer cambios de GitHub | `git pull origin main` |

---

*Ante cualquier duda, consulta con el líder del proyecto antes de hacer cambios en `main`.*
