/*
  pygame - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  Pete Shinners
  pete@shinners.org
*/


/*
 *  font module for pygame
 */
#define PYGAMEAPI_FONT_INTERNAL
#include "font.h"
#include <stdio.h>
#include <string.h>
#include "pygame.h"
#include "pgcompat.h"
#include "pygamedocs.h"
#include "structmember.h"

static PyTypeObject PyFont_Type;
static PyObject* PyFont_New (TTF_Font*);
#define PyFont_Check(x) ((x)->ob_type == &PyFont_Type)

static int font_initialized = 0;
#ifndef __SYMBIAN32__
static const char const *font_defaultname = "freesansbold.ttf";
static const char const *pkgdatamodule_name = "pygame.pkgdata";
static const char const *resourcefunc_name = "getResource";
#else
/// Symbian GCCE does not like the second const
static const char *font_defaultname = "freesansbold.ttf";
static const char *pkgdatamodule_name = "pygame.pkgdata";
static const char *resourcefunc_name = "getResource";
#endif


static PyObject*
font_resource (const char *filename)
{
    PyObject* load_basicfunc = NULL;
    PyObject* pkgdatamodule = NULL;
    PyObject* resourcefunc = NULL;
    PyObject* result = NULL;
#if PY3
    PyObject* tmp;
#endif

    pkgdatamodule = PyImport_ImportModule (pkgdatamodule_name);
    if (!pkgdatamodule)
        goto font_resource_end;

    resourcefunc = PyObject_GetAttrString (pkgdatamodule, resourcefunc_name);
    if (!resourcefunc)
        goto font_resource_end;

    result = PyObject_CallFunction (resourcefunc, "s", filename);
    if (!result)
        goto font_resource_end;

#if PY3
    tmp = PyObject_GetAttrString (result, "name");
    if (tmp != NULL) {
        Py_DECREF (result);
        result = tmp;
    }
    else {
        PyErr_Clear ();
    }
#else
    if (PyFile_Check (result))
    {		
        PyObject *tmp = PyFile_Name (result);        
        Py_INCREF (tmp);
        Py_DECREF (result);
        result = tmp;
    }
#endif

font_resource_end:
    Py_XDECREF (pkgdatamodule);
    Py_XDECREF (resourcefunc);
    Py_XDECREF (load_basicfunc);
    return result;
}

static void
font_autoquit (void)
{
    if (font_initialized)
    {
        font_initialized = 0;
        TTF_Quit ();
    }
}


static PyObject*
font_autoinit (PyObject* self)
{
    if (!font_initialized)
    {
        PyGame_RegisterQuit (font_autoquit);

        if (TTF_Init ())
            return PyInt_FromLong (0);
        font_initialized = 1;

    }
    return PyInt_FromLong (font_initialized);
}

static PyObject*
fontmodule_quit (PyObject* self)
{
    font_autoquit ();
    Py_RETURN_NONE;
}


static PyObject*
fontmodule_init (PyObject* self)
{
    PyObject* result;
    int istrue;

    result = font_autoinit (self);
    istrue = PyObject_IsTrue (result);
    Py_DECREF (result);
    if (!istrue)
        return RAISE (PyExc_SDLError, SDL_GetError ());
    Py_RETURN_NONE;
}

static PyObject*
get_init (PyObject* self)
{
    return PyInt_FromLong (font_initialized);
}

/* font object methods */
static PyObject*
font_get_height (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong (TTF_FontHeight (font));
}

static PyObject*
font_get_descent (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong (TTF_FontDescent (font));
}

static PyObject*
font_get_ascent (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong (TTF_FontAscent (font));
}

static PyObject*
font_get_linesize (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong (TTF_FontLineSkip (font));
}

static PyObject*
font_get_bold (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong ((TTF_GetFontStyle (font) & TTF_STYLE_BOLD) != 0);
}

static PyObject*
font_set_bold (PyObject* self, PyObject* args)
{
    TTF_Font* font = PyFont_AsFont (self);
    int style, val;

    if (!PyArg_ParseTuple (args, "i", &val))
        return NULL;

    style = TTF_GetFontStyle (font);
    if (val)
        style |= TTF_STYLE_BOLD;
    else
        style &= ~TTF_STYLE_BOLD;
    TTF_SetFontStyle (font, style);

    Py_RETURN_NONE;
}

static PyObject*
font_get_italic (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong ((TTF_GetFontStyle (font) & TTF_STYLE_ITALIC) != 0);
}

static PyObject*
font_set_italic (PyObject* self, PyObject* args)
{
    TTF_Font* font = PyFont_AsFont (self);
    int style, val;

    if (!PyArg_ParseTuple (args, "i", &val))
        return NULL;

    style = TTF_GetFontStyle (font);
    if(val)
        style |= TTF_STYLE_ITALIC;
    else
        style &= ~TTF_STYLE_ITALIC;
    TTF_SetFontStyle (font, style);

    Py_RETURN_NONE;
}

static PyObject*
font_get_underline (PyObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);
    return PyInt_FromLong
        ((TTF_GetFontStyle (font) & TTF_STYLE_UNDERLINE) != 0);
}

static PyObject*
font_set_underline (PyObject* self, PyObject* args)
{
    TTF_Font* font = PyFont_AsFont (self);
    int style, val;

    if (!PyArg_ParseTuple (args, "i", &val))
        return NULL;

    style = TTF_GetFontStyle (font);
    if(val)
        style |= TTF_STYLE_UNDERLINE;
    else
        style &= ~TTF_STYLE_UNDERLINE;
    TTF_SetFontStyle (font, style);

    Py_RETURN_NONE;
}

static PyObject*
font_render (PyObject* self, PyObject* args)
{
    TTF_Font* font = PyFont_AsFont (self);
    int aa;
    PyObject* text, *final;
    PyObject* fg_rgba_obj, *bg_rgba_obj = NULL;
    Uint8 rgba[4];
    SDL_Surface* surf;
    SDL_Color foreg, backg;
    int just_return;
    just_return = 0;

    if (!PyArg_ParseTuple (args, "OiO|O", &text, &aa, &fg_rgba_obj,
                           &bg_rgba_obj))
        return NULL;

    if (!RGBAFromColorObj (fg_rgba_obj, rgba))
        return RAISE (PyExc_TypeError, "Invalid foreground RGBA argument");
    foreg.r = rgba[0];
    foreg.g = rgba[1];
    foreg.b = rgba[2];
    if (bg_rgba_obj)
    {
        if (!RGBAFromColorObj (bg_rgba_obj, rgba))
            return RAISE (PyExc_TypeError, "Invalid background RGBA argument");
        backg.r = rgba[0];
        backg.g = rgba[1];
        backg.b = rgba[2];
        backg.unused = 0;
    }
    else
    {
        backg.r = 0;
        backg.g = 0;
        backg.b = 0;
        backg.unused = 0;
    }

    if (!PyObject_IsTrue (text))
    {
        int height = TTF_FontHeight (font);

        surf = SDL_CreateRGBSurface (SDL_SWSURFACE, 1, height, 32,
                                     0xff<<16, 0xff<<8, 0xff, 0);
        if (!surf)
            return RAISE (PyExc_SDLError, "SDL_CreateRGBSurface failed");

        if (bg_rgba_obj)
        {

            Uint32 c = SDL_MapRGB (surf->format, backg.r, backg.g, backg.b);
            SDL_FillRect (surf, NULL, c);
        }
        else
            SDL_SetColorKey (surf, SDL_SRCCOLORKEY, 0);
        just_return = 1;
    }
    else if (PyUnicode_Check (text))
    {
        PyObject* strob = PyUnicode_AsEncodedString (text, "utf-8", "replace");
        char *astring = Bytes_AsString (strob);

        if (aa)
        {
            if (!bg_rgba_obj)
                surf = TTF_RenderUTF8_Blended (font, astring, foreg);
            else
                surf = TTF_RenderUTF8_Shaded (font, astring, foreg, backg);
        }
        else
            surf = TTF_RenderUTF8_Solid (font, astring, foreg);

        Py_DECREF (strob);
    }
    else if (Bytes_Check (text))
    {
        char* astring = Bytes_AsString (text);

        if (aa)
        {
            if (!bg_rgba_obj)
                surf = TTF_RenderText_Blended (font, astring, foreg);
            else
                surf = TTF_RenderText_Shaded (font, astring, foreg, backg);
        }
        else
            surf = TTF_RenderText_Solid (font, astring, foreg);
    }
    else
        return RAISE (PyExc_TypeError, "text must be a string or unicode");

    if (!surf)
        return RAISE (PyExc_SDLError, TTF_GetError());

    if (!aa && bg_rgba_obj && !just_return) /*turn off transparancy*/
    {
        SDL_SetColorKey (surf, 0, 0);
        surf->format->palette->colors[0].r = backg.r;
        surf->format->palette->colors[0].g = backg.g;
        surf->format->palette->colors[0].b = backg.b;
    }

    final = PySurface_New (surf);
    if (!final)
        SDL_FreeSurface (surf);
    return final;
}

static PyObject*
font_size (PyObject* self, PyObject* args)
{
    TTF_Font* font = PyFont_AsFont (self);
    int w, h;
    PyObject* text;

    if (!PyArg_ParseTuple (args, "O", &text))
        return NULL;

    if (PyUnicode_Check (text))
    {
        //PyObject* strob = PyUnicode_AsEncodedObject(text, "utf-8", "replace");
        PyObject* strob = PyUnicode_AsEncodedString (text, "utf-8", "replace");
        char *string = Bytes_AsString (strob);

        TTF_SizeUTF8 (font, string, &w, &h);
        Py_DECREF (strob);
    }
    else if (Bytes_Check (text))
    {
        char* string = Bytes_AsString (text);
        TTF_SizeText (font, string, &w, &h);
    }
    else
        return RAISE (PyExc_TypeError, "text must be a string or unicode");

    return Py_BuildValue ("(ii)", w, h);
}

static PyObject*
font_metrics (PyObject* self, PyObject* args)
{
    TTF_Font *font = PyFont_AsFont (self);
    PyObject *list;
    PyObject *textobj;
    int length;
    int i;
    int minx;
    int maxx;
    int miny;
    int maxy;
    int advance;
    void *buf;
    int isunicode = 0;

    if (!PyArg_ParseTuple (args, "O", &textobj))
        return NULL;

    if (PyUnicode_Check (textobj))
    {
        buf = PyUnicode_AsUnicode (textobj);
        isunicode = 1;
    }
    else if (Bytes_Check (textobj))
        buf = Bytes_AsString (textobj);
    else
        return RAISE (PyExc_TypeError, "text must be a string or unicode");

    if (!buf)
        return NULL;

    if (isunicode)
        length = PyUnicode_GetSize (textobj);
    else
        length = Bytes_Size (textobj);

    if (length == 0)
        Py_RETURN_NONE;

    list = PyList_New (length);
    if (isunicode)
    {
        for (i = 0; i < length; i++)
        {
            /* TODO:
             * TTF_GlyphMetrics() seems to returns a value for any character,
             * using the default invalid character, if the char is not found.
             */
            if (TTF_GlyphMetrics (font, (Uint16) ((Py_UNICODE*) buf)[i], &minx,
                                  &maxx, &miny, &maxy, &advance) == -1)
            {
                Py_INCREF (Py_None);
                PyList_SetItem (list, i, Py_None); /* No matching metrics. */
            }
            else
            {
                PyList_SetItem (list, i, Py_BuildValue
                                ("(iiiii)", minx, maxx, miny, maxy, advance));
            }
        }
    }
    else
    {
        for (i = 0; i < length; i++)
        {
            /* TODO:
             * TTF_GlyphMetrics() seems to returns a value for any character,
             * using the default invalid character, if the char is not found.
             */
            if (TTF_GlyphMetrics (font, (Uint16) ((char*) buf)[i], &minx,
                                  &maxx, &miny, &maxy, &advance) == -1)
            {
                Py_INCREF (Py_None);
                PyList_SetItem (list, i, Py_None); /* No matching metrics. */
            }
            else
            {
                PyList_SetItem (list, i, Py_BuildValue
                                ("(iiiii)", minx, maxx, miny, maxy, advance));
            }
        }
    }
    return list;
}

static PyMethodDef font_methods[] =
{
    { "get_height", (PyCFunction) font_get_height, METH_NOARGS,
      DOC_FONTGETHEIGHT },
    { "get_descent", (PyCFunction) font_get_descent, METH_NOARGS,
      DOC_FONTGETDESCENT },
    { "get_ascent", (PyCFunction) font_get_ascent, METH_NOARGS,
      DOC_FONTGETASCENT },
    { "get_linesize", (PyCFunction) font_get_linesize, METH_NOARGS,
      DOC_FONTGETLINESIZE },

    { "get_bold", (PyCFunction) font_get_bold, METH_NOARGS,
      DOC_FONTGETBOLD },
    { "set_bold", font_set_bold, METH_VARARGS, DOC_FONTSETBOLD },
    { "get_italic", (PyCFunction) font_get_italic, METH_NOARGS,
      DOC_FONTGETITALIC },
    { "set_italic", font_set_italic, METH_VARARGS, DOC_FONTSETITALIC },
    { "get_underline", (PyCFunction) font_get_underline, METH_NOARGS,
      DOC_FONTGETUNDERLINE },
    { "set_underline", font_set_underline, METH_VARARGS, DOC_FONTSETUNDERLINE },

    { "metrics", font_metrics, METH_VARARGS, DOC_FONTMETRICS },
    { "render", font_render, METH_VARARGS, DOC_FONTRENDER },
    { "size", font_size, METH_VARARGS, DOC_FONTSIZE },

    { NULL, NULL, 0, NULL }
};

/*font object internals*/
static void
font_dealloc (PyFontObject* self)
{
    TTF_Font* font = PyFont_AsFont (self);

    if (font && font_initialized)
        TTF_CloseFont (font);

    if (self->weakreflist)
        PyObject_ClearWeakRefs ((PyObject*) self);
    Py_TYPE(self)->tp_free ((PyObject*) self);
}

static int
font_init (PyFontObject *self, PyObject *args, PyObject *kwds)
{
    int fontsize;
    TTF_Font* font = NULL;
    PyObject* fileobj;
    
    self->font = NULL;
    if (!PyArg_ParseTuple (args, "Oi", &fileobj, &fontsize))
        return -1;

    if (!font_initialized)
    {
        RAISE (PyExc_SDLError, "font not initialized");
        return -1;
    }

    Py_INCREF (fileobj);

    if (fontsize <= 1)
        fontsize = 1;

    if (fileobj == Py_None)
    {

        fileobj = font_resource (font_defaultname);
        if (!fileobj)
        {
            char error[1024];
            PyOS_snprintf (error, 1024, "default font not found '%s'",
                      font_defaultname);
            RAISE (PyExc_RuntimeError, error);
            goto error;
        }
        fontsize = (int) (fontsize * .6875);
        if (fontsize <= 1)
            fontsize = 1;
    }
     
    if (PyUnicode_Check (fileobj)) {
        PyObject* tmp = PyUnicode_AsASCIIString (fileobj);

        if (tmp == NULL) {
            goto error;
        }
        fileobj = tmp;
    }

    if (Bytes_Check (fileobj))
    {
        FILE* test;        
        char* filename = Bytes_AsString (fileobj);
       		
        if (!filename) {
            goto error;
        }
                
        /*check if it is a valid file, else SDL_ttf segfaults*/
        test = fopen (filename, "rb");
        if(!test)
        {
            PyObject *tmp = NULL;

            if (!strcmp (filename, font_defaultname)) {
                tmp = font_resource (font_defaultname);
            }
            if (!tmp)
            {
                PyErr_SetString (PyExc_IOError,
                                 "unable to read font filename");
                goto error;
            }
            Py_DECREF (fileobj);
            fileobj = tmp;
        }
        else
        {
            fclose (test);
            Py_BEGIN_ALLOW_THREADS;
            font = TTF_OpenFont(filename, fontsize);
            Py_END_ALLOW_THREADS;
        }	
    }
    if (!font)
    {
#ifdef TTF_MAJOR_VERSION
        SDL_RWops *rw;
        rw = RWopsFromPython (fileobj);
        if (!rw)
        {
            goto error;
        }
        Py_BEGIN_ALLOW_THREADS;
        font = TTF_OpenFontIndexRW (rw, 1, fontsize, 0);
        Py_END_ALLOW_THREADS;
#else
        RAISE (PyExc_NotImplementedError,
               "nonstring fonts require SDL_ttf-2.0.6");
        goto error;
#endif
    }

    if (!font)
    {
        RAISE (PyExc_RuntimeError, SDL_GetError ());
        goto error;
    }

    Py_DECREF (fileobj);
    self->font = font;
    return 0;

error:
    Py_DECREF (fileobj);
    return -1;
}

static PyTypeObject PyFont_Type =
{
    TYPE_HEAD (NULL, 0)
    "pygame.font.Font",
    sizeof(PyFontObject),
    0,
    (destructor)font_dealloc,
    0,
    0, /*getattr*/
    0,
    0,
    0,
    0,
    NULL,
    0,
    (hashfunc)NULL,
    (ternaryfunc)NULL,
    (reprfunc)NULL,
    0L,0L,0L,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    DOC_PYGAMEFONTFONT, /* Documentation string */
    0,					/* tp_traverse */
    0,					/* tp_clear */
    0,					/* tp_richcompare */
    offsetof(PyFontObject, weakreflist),    /* tp_weaklistoffset */
    0,					/* tp_iter */
    0,					/* tp_iternext */
    font_methods,			        /* tp_methods */
    0,				        /* tp_members */
    0,				        /* tp_getset */
    0,					/* tp_base */
    0,					/* tp_dict */
    0,					/* tp_descr_get */
    0,					/* tp_descr_set */
    0,					/* tp_dictoffset */
    (initproc)font_init,			/* tp_init */
    0,					/* tp_alloc */
    0,	                /* tp_new */
};

//PyType_GenericNew,	                /* tp_new */

/*font module methods*/
static PyObject*
get_default_font (PyObject* self)
{
    return Text_FromUTF8 (font_defaultname);
}

static PyMethodDef _font_methods[] =
{
    { "__PYGAMEinit__", (PyCFunction) font_autoinit, METH_NOARGS,
      "auto initialize function for font" },
    { "init", (PyCFunction) fontmodule_init, METH_NOARGS, DOC_PYGAMEFONTINIT },
    { "quit", (PyCFunction) fontmodule_quit, METH_NOARGS, DOC_PYGAMEFONTQUIT },
    { "get_init", (PyCFunction) get_init, METH_NOARGS, DOC_PYGAMEFONTGETINIT },
    { "get_default_font", (PyCFunction) get_default_font, METH_NOARGS,
      DOC_PYGAMEFONTGETDEFAULTFONT },
    { NULL, NULL, 0, NULL }
};



static PyObject*
PyFont_New (TTF_Font* font)
{
    PyFontObject* fontobj;

    if (!font)
        return RAISE (PyExc_RuntimeError, "unable to load font.");
    fontobj = (PyFontObject *) PyFont_Type.tp_new (&PyFont_Type, NULL, NULL);

    if (fontobj)
        fontobj->font = font;

    return (PyObject*) fontobj;
}

MODINIT_DEFINE (font)
{
    PyObject *module, *apiobj;
    static void* c_api[PYGAMEAPI_FONT_NUMSLOTS];

#if PY3
    static struct PyModuleDef _module = {
        PyModuleDef_HEAD_INIT,
        "font",
        DOC_PYGAMEFONT,
        -1,
        _font_methods,
        NULL, NULL, NULL, NULL
    };
#endif

    PyFONT_C_API[0] = PyFONT_C_API[0]; /*clean an unused warning*/

    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base ();
    if (PyErr_Occurred ()) {
	MODINIT_ERROR;
    }
    import_pygame_color ();
    if (PyErr_Occurred ()) {
	MODINIT_ERROR;
    }
    import_pygame_surface ();
    if (PyErr_Occurred ()) {
	MODINIT_ERROR;
    }
    import_pygame_rwobject ();
    if (PyErr_Occurred ()) {
	MODINIT_ERROR;
    }

    /* type preparation */
    if (PyType_Ready (&PyFont_Type) < 0) {
        MODINIT_ERROR;
    }
    PyFont_Type.tp_new = PyType_GenericNew;

#if PY3
    module = PyModule_Create (&_module);
#else
    module = Py_InitModule3 (MODPREFIX "font", 
                             _font_methods, 
                             DOC_PYGAMEFONT);
#endif
    if (module == NULL) {
        MODINIT_ERROR;
    }

    Py_INCREF ((PyObject*) &PyFont_Type);
    if (PyModule_AddObject (module,
                            "FontType",
                            (PyObject *) &PyFont_Type) == -1) {
        Py_DECREF ((PyObject *) &PyFont_Type);
        DECREF_MOD (module);
        MODINIT_ERROR;
    }

    Py_INCREF ((PyObject*) &PyFont_Type);
    if (PyModule_AddObject (module,
                            "Font",
                            (PyObject *) &PyFont_Type) == -1) {
        Py_DECREF ((PyObject *) &PyFont_Type);
        DECREF_MOD (module);
        MODINIT_ERROR;
    }

    /* export the c api */
    c_api[0] = &PyFont_Type;
    c_api[1] = PyFont_New;
    c_api[2] = &font_initialized;
    apiobj = PyCObject_FromVoidPtr (c_api, NULL);
    if (apiobj == NULL) {
        DECREF_MOD (module);
        MODINIT_ERROR;
    }
    if (PyModule_AddObject (module, PYGAMEAPI_LOCAL_ENTRY, apiobj) == -1) {
        Py_DECREF (apiobj);
        DECREF_MOD (module);
        MODINIT_ERROR;
    }
    MODINIT_RETURN (module);
}
