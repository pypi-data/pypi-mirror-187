#include <Python.h>
#include <structmember.h>

#include <SDL.h>
#include <SDL_opengl.h>

#include <imgui.h>
#include <imgui_impl_sdl.h>
#include <imgui_impl_opengl3.h>

PFNGLBINDFRAMEBUFFERPROC glBindFramebuffer;

struct MainWindow {
    PyObject_HEAD
    PyObject * size;
    PyObject * ratio;
    PyObject * mouse;
    PyObject * mouse_delta;
    PyObject * mouse_wheel;
    PyObject * frame;
    PyObject * text;
    PyObject * config;
    PyObject * tooltip;
    PyObject * log;
};

PyTypeObject * MainWindow_type;

SDL_Window * window;
float sidebar_width;
bool closed;
int mouse_x;
int mouse_y;
int mouse_dx;
int mouse_dy;
int mouse_wheel;
int frame;
bool key_down[280];
bool prev_key_down[280];
char text[1024];

PyObject * image_list;
PyObject * config_list;

PyObject * keys;
PyObject * empty_str;

MainWindow * meth_main_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    const char * keywords[] = {"size", "sidebar", "title", NULL};

    int width = 0;
    int height = 0;
    int sidebar = 400;
    const char * title = "Mollia Window";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|(II)Is", (char **)keywords, &width, &height, &sidebar, &title)) {
        return NULL;
    }

    if (window) {
        PyErr_Format(PyExc_RuntimeError, "main window already exists");
        return NULL;
    }

    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER | SDL_INIT_GAMECONTROLLER);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, 0);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3);

    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8);

    if (!width && !height) {
        SDL_DisplayMode display_mode;
        SDL_GetCurrentDisplayMode(0, &display_mode);
        width = display_mode.w - 120;
        height = display_mode.h - 120;
    }

    int window_flags = SDL_WINDOW_OPENGL | SDL_WINDOW_ALLOW_HIGHDPI;
    window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, window_flags);
    SDL_GLContext gl_context = SDL_GL_CreateContext(window);
    SDL_GL_MakeCurrent(window, gl_context);
    SDL_GL_SetSwapInterval(1);

    glBindFramebuffer = (PFNGLBINDFRAMEBUFFERPROC)SDL_GL_GetProcAddress("glBindFramebuffer");

    const unsigned B = 0xff000000;
    const unsigned W = 0xffffffff;
    const unsigned R = 0xff0000d4;
    unsigned pixels[1024] = {
        B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, B, B, B, B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, B, B, B, B, B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, B, B, B, B, B, B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, B, B, B, B, B, B, B, B, W, W, W, W, W, W, R, R, R, R, R, R, W, W, W, W, W, W, B, B,
        B, B, W, B, B, B, B, W, B, B, B, B, W, W, W, W, R, R, R, R, R, R, R, R, R, R, W, W, W, W, B, B,
        B, B, B, B, B, B, W, W, B, B, B, B, W, W, W, R, R, R, R, R, R, R, R, R, R, R, R, W, W, W, B, B,
        B, B, B, B, B, W, W, W, B, B, B, B, W, W, W, R, R, R, R, R, R, R, R, R, R, R, R, W, W, W, B, B,
        B, B, B, B, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, B, W, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, R, R, R, R, R, R, R, R, R, R, R, R, R, R, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, W, R, R, R, R, R, R, R, R, R, R, R, R, W, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, W, R, R, R, R, R, R, R, R, R, R, R, R, W, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, W, W, R, R, R, R, R, R, R, R, R, R, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, B, B, B, B, W, W, W, W, W, W, R, R, R, R, R, R, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, B, B,
        B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B,
    };

    SDL_Surface * surface = SDL_CreateRGBSurfaceFrom(pixels, 32, 32, 32, 128, 0xff, 0xff00, 0xff0000, 0xff000000);
    SDL_SetWindowIcon(window, surface);
    SDL_FreeSurface(surface);

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGui::StyleColorsDark();
    ImGui::GetStyle().Colors[ImGuiCol_TitleBgActive] = ImGui::GetStyle().Colors[ImGuiCol_TitleBg];
    ImGui::GetStyle().Colors[ImGuiCol_TitleBgCollapsed] = ImGui::GetStyle().Colors[ImGuiCol_TitleBg];
    ImGui::GetStyle().WindowBorderSize = 0.0f;

    ImGuiIO & io = ImGui::GetIO();
    io.IniFilename = NULL;

    ImGui_ImplSDL2_InitForOpenGL(window, gl_context);
    ImGui_ImplOpenGL3_Init("#version 130");

    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplSDL2_NewFrame();
    ImGui::NewFrame();

    MainWindow * res = PyObject_New(MainWindow, MainWindow_type);
    res->size = Py_BuildValue("(II)", width - sidebar, height);
    res->ratio = PyFloat_FromDouble((double)(width - sidebar) / (double)height);
    res->mouse = Py_BuildValue("(ii)", 0, 0);
    res->mouse_delta = Py_BuildValue("(ii)", 0, 0);
    res->mouse_wheel = PyLong_FromLong(0);
    res->frame = PyLong_FromLong(0);

    Py_INCREF(empty_str);
    res->text = empty_str;

    PyObject * pyio = PyImport_ImportModule("io");
    res->log = PyObject_CallMethod(pyio, "StringIO", NULL);

    res->tooltip = NULL;
    res->config = PyDict_New();
    sidebar_width = (float)sidebar;

    Py_INCREF(res);
    PyModule_AddObject(self, "wnd", (PyObject *)res);

    return res;
}

int sdl_key(int key) {
    switch (key) {
        case SDLK_TAB: return 9;
        case SDLK_LEFT: return 37;
        case SDLK_RIGHT: return 39;
        case SDLK_UP: return 38;
        case SDLK_DOWN: return 40;
        case SDLK_PAGEUP: return 33;
        case SDLK_PAGEDOWN: return 34;
        case SDLK_HOME: return 36;
        case SDLK_END: return 35;
        case SDLK_INSERT: return 45;
        case SDLK_DELETE: return 46;
        case SDLK_BACKSPACE: return 8;
        case SDLK_SPACE: return 32;
        case SDLK_RETURN: return 13;
        case SDLK_ESCAPE: return 27;
        case SDLK_QUOTE: return 222;
        case SDLK_COMMA: return 188;
        case SDLK_MINUS: return 189;
        case SDLK_PERIOD: return 190;
        case SDLK_SLASH: return 191;
        case SDLK_SEMICOLON: return 186;
        case SDLK_EQUALS: return 187;
        case SDLK_LEFTBRACKET: return 219;
        case SDLK_BACKSLASH: return 220;
        case SDLK_RIGHTBRACKET: return 221;
        case SDLK_BACKQUOTE: return 192;
        case SDLK_CAPSLOCK: return 20;
        case SDLK_SCROLLLOCK: return 145;
        case SDLK_NUMLOCKCLEAR: return 144;
        case SDLK_PRINTSCREEN: return 44;
        case SDLK_PAUSE: return 19;
        case SDLK_KP_0: return 96;
        case SDLK_KP_1: return 97;
        case SDLK_KP_2: return 98;
        case SDLK_KP_3: return 99;
        case SDLK_KP_4: return 100;
        case SDLK_KP_5: return 101;
        case SDLK_KP_6: return 102;
        case SDLK_KP_7: return 103;
        case SDLK_KP_8: return 104;
        case SDLK_KP_9: return 105;
        case SDLK_KP_PERIOD: return 110;
        case SDLK_KP_DIVIDE: return 111;
        case SDLK_KP_MULTIPLY: return 106;
        case SDLK_KP_MINUS: return 109;
        case SDLK_KP_PLUS: return 107;
        case SDLK_KP_ENTER: return 269;
        case SDLK_KP_EQUALS: return 160;
        case SDLK_LCTRL: return 162;
        case SDLK_LSHIFT: return 164;
        case SDLK_LALT: return 91;
        case SDLK_LGUI: return 161;
        case SDLK_RCTRL: return 163;
        case SDLK_RSHIFT: return 165;
        case SDLK_RALT: return 92;
        case SDLK_RGUI: return 93;
        case SDLK_0: return 48;
        case SDLK_1: return 49;
        case SDLK_2: return 50;
        case SDLK_3: return 51;
        case SDLK_4: return 52;
        case SDLK_5: return 53;
        case SDLK_6: return 54;
        case SDLK_7: return 55;
        case SDLK_8: return 56;
        case SDLK_9: return 57;
        case SDLK_a: return 65;
        case SDLK_b: return 66;
        case SDLK_c: return 67;
        case SDLK_d: return 68;
        case SDLK_e: return 69;
        case SDLK_f: return 70;
        case SDLK_g: return 71;
        case SDLK_h: return 72;
        case SDLK_i: return 73;
        case SDLK_j: return 74;
        case SDLK_k: return 75;
        case SDLK_l: return 76;
        case SDLK_m: return 77;
        case SDLK_n: return 78;
        case SDLK_o: return 79;
        case SDLK_p: return 80;
        case SDLK_q: return 81;
        case SDLK_r: return 82;
        case SDLK_s: return 83;
        case SDLK_t: return 84;
        case SDLK_u: return 85;
        case SDLK_v: return 86;
        case SDLK_w: return 87;
        case SDLK_x: return 88;
        case SDLK_y: return 89;
        case SDLK_z: return 90;
        case SDLK_F1: return 112;
        case SDLK_F2: return 113;
        case SDLK_F3: return 114;
        case SDLK_F4: return 115;
        case SDLK_F5: return 116;
        case SDLK_F6: return 117;
        case SDLK_F7: return 118;
        case SDLK_F8: return 119;
        case SDLK_F9: return 120;
        case SDLK_F10: return 121;
        case SDLK_F11: return 122;
        case SDLK_F12: return 123;
    }
    return 0;
}

PyObject * MainWindow_meth_update(MainWindow * self) {
    if (closed) {
        Py_RETURN_FALSE;
    }

    ImGuiIO & io = ImGui::GetIO();

    int image_count = (int)PyList_Size(image_list);
    for (int i = 0; i < image_count; ++i) {
        PyObject * obj = PyList_GET_ITEM(image_list, i);
        PyObject * name = PyDict_GetItemString(obj, "name");
        ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, {2.0f, 2.0f});
        if (ImGui::Begin(PyUnicode_AsUTF8(name), NULL, ImGuiWindowFlags_NoResize)) {
            int texture = PyLong_AsLong(PyDict_GetItemString(obj, "texture"));
            bool flip = PyObject_IsTrue(PyDict_GetItemString(obj, "flip"));
            float x = (float)PyFloat_AsDouble(PyDict_GetItemString(obj, "x"));
            float y = (float)PyFloat_AsDouble(PyDict_GetItemString(obj, "y"));
            float width = (float)PyFloat_AsDouble(PyDict_GetItemString(obj, "width"));
            float height = (float)PyFloat_AsDouble(PyDict_GetItemString(obj, "height"));
            ImGui::SetWindowPos({x, y}, ImGuiCond_Once);
            if (flip) {
                ImGui::Image((ImTextureID)(long long)texture, {width, height}, {0.0f, 1.0f}, {1.0f, 0.0f});
            } else {
                ImGui::Image((ImTextureID)(long long)texture, {width, height});
            }
            ImGui::End();
        }
        ImGui::PopStyleVar();
    }

    ImGui::SetNextWindowPos({io.DisplaySize.x - sidebar_width, 0.0f});
    ImGui::SetNextWindowSize({sidebar_width, io.DisplaySize.y});
    ImGui::Begin("Sidebar", NULL, ImGuiWindowFlags_NoBringToFrontOnFocus | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoCollapse);
    ImGui::SetNextItemOpen(true, ImGuiCond_Once);
    bool config_open = ImGui::CollapsingHeader("Config");
    int config_count = (int)PyList_Size(config_list);
    for (int i = 0; i < config_count; ++i) {
        PyObject * obj = PyList_GET_ITEM(config_list, i);
        PyObject * name = PyDict_GetItemString(obj, "name");
        PyObject * type = PyDict_GetItemString(obj, "type");
        if (!PyUnicode_CompareWithASCIIString(type, "group")) {
            config_open = ImGui::CollapsingHeader(PyUnicode_AsUTF8(name));
        }
        if (!config_open) {
            continue;
        }
        if (!PyUnicode_CompareWithASCIIString(type, "slider")) {
            double value = PyFloat_AsDouble(PyDict_GetItem(self->config, name));
            double min_value = PyFloat_AsDouble(PyDict_GetItemString(obj, "min"));
            double max_value = PyFloat_AsDouble(PyDict_GetItemString(obj, "max"));
            const char * format = PyUnicode_AsUTF8(PyDict_GetItemString(obj, "format"));
            if (ImGui::SliderScalar(PyUnicode_AsUTF8(name), ImGuiDataType_Double, &value, &min_value, &max_value, format)) {
                value = value > min_value ? value : min_value;
                value = value < max_value ? value : max_value;
                PyObject * new_value = PyFloat_FromDouble(value);
                PyDict_SetItem(self->config, name, new_value);
                Py_DECREF(new_value);
            }
        }
        if (!PyUnicode_CompareWithASCIIString(type, "increment")) {
            int value = PyLong_AsLong(PyDict_GetItem(self->config, name));
            int min_value = PyLong_AsLong(PyDict_GetItemString(obj, "min"));
            int max_value = PyLong_AsLong(PyDict_GetItemString(obj, "max"));
            int step = PyLong_AsLong(PyDict_GetItemString(obj, "step"));
            if (ImGui::InputScalar(PyUnicode_AsUTF8(name), ImGuiDataType_S32, &value, &step, NULL, NULL)) {
                value = value > min_value ? value : min_value;
                value = value < max_value ? value : max_value;
                PyObject * new_value = PyLong_FromLong(value);
                PyDict_SetItem(self->config, name, new_value);
                Py_DECREF(new_value);
            }
        }
        if (!PyUnicode_CompareWithASCIIString(type, "checkbox")) {
            bool value = PyObject_IsTrue(PyDict_GetItem(self->config, name));
            if (ImGui::Checkbox(PyUnicode_AsUTF8(name), &value)) {
                PyDict_SetItem(self->config, name, value ? Py_True : Py_False);
            }
        }
        if (!PyUnicode_CompareWithASCIIString(type, "combo")) {
            PyObject * value = PyDict_GetItem(self->config, name);
            PyObject * options = PyDict_GetItemString(obj, "options");
            int index = (int)PySequence_Index(options, value);
            if (index < 0) {
                return NULL;
            }
            int num_items = (int)PyList_Size(options);
            const char * items[256];
            for (int i = 0; i < num_items; ++i) {
                items[i] = PyUnicode_AsUTF8(PyList_GetItem(options, i));
            }
            if (ImGui::Combo(PyUnicode_AsUTF8(name), &index, items, num_items)) {
                PyDict_SetItem(self->config, name, PyList_GetItem(options, index));
            }
        }
        if (!PyUnicode_CompareWithASCIIString(type, "button")) {
            if (ImGui::Button(PyUnicode_AsUTF8(name))) {
                PyObject * click = PyDict_GetItemString(obj, "click");
                PyObject * res = PyObject_CallFunction(click, NULL);
                if (!res) {
                    return NULL;
                }
                Py_DECREF(res);
            }
        }
    }

    Py_DECREF(PyObject_CallMethod(self->log, "truncate", NULL));

    ImGui::SetNextItemOpen(true, ImGuiCond_Once);
    if (ImGui::CollapsingHeader("Log")) {
        Py_ssize_t size = 0;
        PyObject * text = PyObject_CallMethod(self->log, "getvalue", NULL);
        const char * ptr = PyUnicode_AsUTF8AndSize(text, &size);
        ImGui::TextUnformatted(ptr, ptr + size);
        Py_DECREF(text);
    }
    Py_DECREF(PyObject_CallMethod(self->log, "seek", "i", 0));
    ImGui::End();

    if (self->tooltip) {
        ImGui::BeginTooltip();
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(PyUnicode_AsUTF8(self->tooltip));
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
        Py_DECREF(self->tooltip);
        self->tooltip = NULL;
    }

    ImGui::Render();

    int draw_fbo = 0;
    glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING, &draw_fbo);
    glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0);

    if (glIsEnabled(0x8DB9)) {
        glDisable(0x8DB9);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glEnable(0x8DB9);
    } else {
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
    }

    SDL_GL_SwapWindow(window);

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glBindFramebuffer(GL_DRAW_FRAMEBUFFER, draw_fbo);

    memcpy(prev_key_down, key_down, sizeof(key_down));
    mouse_dx = 0;
    mouse_dy = 0;
    mouse_wheel = 0;
    text[0] = 0;

    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        ImGui_ImplSDL2_ProcessEvent(&event);
        if (event.type == SDL_QUIT || (event.type == SDL_WINDOWEVENT && event.window.event == SDL_WINDOWEVENT_CLOSE && event.window.windowID == SDL_GetWindowID(window))) {
            closed = true;
            Py_RETURN_FALSE;
        }
        switch (event.type) {
            case SDL_TEXTINPUT: {
                ImGuiIO & io = ImGui::GetIO();
                if (!io.WantTextInput) {
                    strcat(text, event.text.text);
                }
                break;
            }
            case SDL_KEYDOWN:
            case SDL_KEYUP: {
                ImGuiIO & io = ImGui::GetIO();
                if (!io.WantCaptureKeyboard) {
                    key_down[sdl_key(event.key.keysym.sym)] = event.key.state == SDL_PRESSED;
                }
                break;
            }
            case SDL_MOUSEBUTTONDOWN:
            case SDL_MOUSEBUTTONUP: {
                ImGuiIO & io = ImGui::GetIO();
                if (!io.WantCaptureMouse) {
                    switch (event.button.button) {
                        case SDL_BUTTON_LEFT: key_down[1] = event.button.state == SDL_PRESSED; break;
                        case SDL_BUTTON_RIGHT: key_down[2] = event.button.state == SDL_PRESSED; break;
                        case SDL_BUTTON_MIDDLE: key_down[4] = event.button.state == SDL_PRESSED; break;
                    }
                }
                break;
            }
            case SDL_MOUSEMOTION: {
                ImGuiIO & io = ImGui::GetIO();
                if (!io.WantCaptureMouse) {
                    mouse_x = event.motion.x;
                    mouse_y = event.motion.y;
                    mouse_dx += event.motion.xrel;
                    mouse_dy += event.motion.yrel;
                }
                break;
            }
            case SDL_MOUSEWHEEL: {
                ImGuiIO & io = ImGui::GetIO();
                if (!io.WantCaptureMouse) {
                    mouse_wheel += event.wheel.y;
                }
                break;
            }
        }
    }

    Py_DECREF(self->mouse);
    Py_DECREF(self->mouse_delta);
    Py_DECREF(self->mouse_wheel);
    Py_DECREF(self->frame);
    Py_DECREF(self->text);

    if (text[0]) {
        self->text = PyUnicode_FromString(text);
    } else {
        Py_INCREF(empty_str);
        self->text = empty_str;
    }

    self->mouse = Py_BuildValue("(ii)", mouse_x, mouse_y);
    self->mouse_delta = Py_BuildValue("(ii)", mouse_dx, mouse_dy);
    self->mouse_wheel = PyLong_FromLong(mouse_wheel);
    self->frame = PyLong_FromLong(frame);

    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplSDL2_NewFrame();
    ImGui::NewFrame();
    frame += 1;

    Py_RETURN_TRUE;
}

int get_key(PyObject * key) {
    if (PyObject * key_code = PyDict_GetItem(keys, key)) {
        return PyLong_AsLong(key_code);
    }
    PyErr_Format(PyExc_ValueError, "no such key %R", key);
    return 0;
}

PyObject * MainWindow_meth_key_pressed(MainWindow * self, PyObject * arg) {
    if (int key = get_key(arg)) {
        if (key_down[key] && !prev_key_down[key]) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }
    return NULL;
}

PyObject * MainWindow_meth_key_released(MainWindow * self, PyObject * arg) {
    if (int key = get_key(arg)) {
        if (!key_down[key] && prev_key_down[key]) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }
    return NULL;
}

PyObject * MainWindow_meth_key_down(MainWindow * self, PyObject * arg) {
    if (int key = get_key(arg)) {
        if (key_down[key]) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }
    return NULL;
}

PyObject * MainWindow_meth_key_up(MainWindow * self, PyObject * arg) {
    if (int key = get_key(arg)) {
        if (!key_down[key]) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }
    return NULL;
}

PyObject * MainWindow_meth_image(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "texture", "position", "size", "flip", NULL};

    const char * name;
    int texture;
    float width, height;
    float x = 0.0f;
    float y = 0.0f;
    int flip = false;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "si(ff)(ff)|$p", keywords, &name, &texture, &x, &y, &width, &height, &flip)) {
        return NULL;
    }

    PyList_Append(image_list, Py_BuildValue(
        "{sssisfsfsfsfsO}",
        "name", name,
        "texture", texture,
        "x", x,
        "y", y,
        "width", width,
        "height", height,
        "flip", flip ? Py_True : Py_False
    ));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_slider(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "value", "min", "max", "format", NULL};

    const char * name;
    double value = 0.0;
    double min_value = -1.0;
    double max_value = 1.0;
    const char * format = "%.2f";

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|d$dds", keywords, &name, &value, &min_value, &max_value, &format)) {
        return NULL;
    }

    PyDict_SetItemString(self->config, name, PyFloat_FromDouble(value));
    PyList_Append(config_list, Py_BuildValue("{sssssdsdss}", "type", "slider", "name", name, "min", min_value, "max", max_value, "format", format));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_increment(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "value", "min", "max", "step", NULL};

    const char * name;
    int value = 0;
    int min_value = 0;
    int max_value = 100;
    int step = 1;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|i$iii", keywords, &name, &value, &min_value, &max_value, &step)) {
        return NULL;
    }

    PyDict_SetItemString(self->config, name, PyLong_FromLong(value));
    PyList_Append(config_list, Py_BuildValue("{sssssisisi}", "type", "increment", "name", name, "min", min_value, "max", max_value, "step", step));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_checkbox(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "value", NULL};

    const char * name;
    int value = false;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|p", keywords, &name, &value)) {
        return NULL;
    }

    PyDict_SetItemString(self->config, name, value ? Py_True : Py_False);
    PyList_Append(config_list, Py_BuildValue("{ssss}", "type", "checkbox", "name", name));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_combo(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "value", "options", NULL};

    const char * name;
    PyObject * value;
    PyObject * options;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "sOO", keywords, &name, &value, &options)) {
        return NULL;
    }

    if (!PyUnicode_CheckExact(value) || !PyList_CheckExact(options)) {
        return NULL;
    }

    for (int i = 0; i < (int)PyList_Size(options); ++i) {
        if (!PyUnicode_CheckExact(PyList_GetItem(options, i))) {
            return NULL;
        }
    }

    PyDict_SetItemString(self->config, name, value);
    PyList_Append(config_list, Py_BuildValue("{sssssO}", "type", "combo", "name", name, "options", options));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_button(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", "click", NULL};

    const char * name;
    PyObject * click;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "sO", keywords, &name, &click)) {
        return NULL;
    }

    if (!PyCallable_Check(click)) {
        return NULL;
    }

    PyList_Append(config_list, Py_BuildValue("{sssssO}", "type", "button", "name", name, "click", click));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_group(MainWindow * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"name", NULL};

    const char * name;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", keywords, &name)) {
        return NULL;
    }

    PyList_Append(config_list, Py_BuildValue("{ssss}", "type", "group", "name", name));
    Py_RETURN_NONE;
}

PyObject * MainWindow_meth_tooltip(MainWindow * self, PyObject * arg) {
    if (!PyUnicode_CheckExact(arg)) {
        return NULL;
    }
    if (!PyUnicode_GetLength(arg)) {
        self->tooltip = NULL;
        Py_RETURN_NONE;
    }
    Py_INCREF(arg);
    Py_XDECREF(self->tooltip);
    self->tooltip = arg;
    Py_RETURN_NONE;
}

void default_dealloc(PyObject * self) {
    Py_TYPE(self)->tp_free(self);
}

PyMethodDef MainWindow_methods[] = {
    {"update", (PyCFunction)MainWindow_meth_update, METH_NOARGS, NULL},
    {"key_pressed", (PyCFunction)MainWindow_meth_key_pressed, METH_O, NULL},
    {"key_released", (PyCFunction)MainWindow_meth_key_released, METH_O, NULL},
    {"key_down", (PyCFunction)MainWindow_meth_key_down, METH_O, NULL},
    {"key_up", (PyCFunction)MainWindow_meth_key_up, METH_O, NULL},
    {"image", (PyCFunction)MainWindow_meth_image, METH_VARARGS | METH_KEYWORDS, NULL},
    {"slider", (PyCFunction)MainWindow_meth_slider, METH_VARARGS | METH_KEYWORDS, NULL},
    {"increment", (PyCFunction)MainWindow_meth_increment, METH_VARARGS | METH_KEYWORDS, NULL},
    {"checkbox", (PyCFunction)MainWindow_meth_checkbox, METH_VARARGS | METH_KEYWORDS, NULL},
    {"combo", (PyCFunction)MainWindow_meth_combo, METH_VARARGS | METH_KEYWORDS, NULL},
    {"button", (PyCFunction)MainWindow_meth_button, METH_VARARGS | METH_KEYWORDS, NULL},
    {"group", (PyCFunction)MainWindow_meth_group, METH_VARARGS | METH_KEYWORDS, NULL},
    {"tooltip", (PyCFunction)MainWindow_meth_tooltip, METH_O, NULL},
    {},
};

PyMemberDef MainWindow_members[] = {
    {"size", T_OBJECT, offsetof(MainWindow, size), READONLY, NULL},
    {"ratio", T_OBJECT, offsetof(MainWindow, ratio), READONLY, NULL},
    {"mouse", T_OBJECT, offsetof(MainWindow, mouse), READONLY, NULL},
    {"mouse_delta", T_OBJECT, offsetof(MainWindow, mouse_delta), READONLY, NULL},
    {"mouse_wheel", T_OBJECT, offsetof(MainWindow, mouse_wheel), READONLY, NULL},
    {"frame", T_OBJECT, offsetof(MainWindow, frame), READONLY, NULL},
    {"text", T_OBJECT, offsetof(MainWindow, text), READONLY, NULL},
    {"log", T_OBJECT, offsetof(MainWindow, log), READONLY, NULL},
    {"config", T_OBJECT, offsetof(MainWindow, config), READONLY, NULL},
    {},
};

PyType_Slot MainWindow_slots[] = {
    {Py_tp_methods, MainWindow_methods},
    {Py_tp_members, MainWindow_members},
    {Py_tp_dealloc, (void *)default_dealloc},
    {},
};

PyType_Spec MainWindow_spec = {"mollia_window.MainWindow", sizeof(MainWindow), 0, Py_TPFLAGS_DEFAULT, MainWindow_slots};

PyMethodDef module_methods[] = {
    {"main_window", (PyCFunction)meth_main_window, METH_VARARGS | METH_KEYWORDS, NULL},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "mollia_window", NULL, -1, module_methods};

void add_key(const char * name, int code) {
    PyObject * key_code = PyLong_FromLong(code);
    PyDict_SetItemString(keys, name, key_code);
    Py_DECREF(key_code);
}

extern "C" PyObject * PyInit_mollia_window() {
    PyObject * module = PyModule_Create(&module_def);

    MainWindow_type = (PyTypeObject *)PyType_FromSpec(&MainWindow_spec);

    Py_INCREF(MainWindow_type);
    PyModule_AddObject(module, "MainWindow", (PyObject *)MainWindow_type);

    image_list = PyList_New(0);
    config_list = PyList_New(0);

    empty_str = PyUnicode_FromString("");
    keys = PyDict_New();

    add_key("mouse1", 1);
    add_key("mouse2", 2);
    add_key("mouse3", 4);
    add_key("tab", 9);
    add_key("left_arrow", 37);
    add_key("right_arrow", 39);
    add_key("up_arrow", 38);
    add_key("down_arrow", 40);
    add_key("pageup", 33);
    add_key("pagedown", 34);
    add_key("home", 36);
    add_key("end", 35);
    add_key("insert", 45);
    add_key("delete", 46);
    add_key("backspace", 8);
    add_key("space", 32);
    add_key("enter", 13);
    add_key("escape", 27);
    add_key("apostrophe", 222);
    add_key("comma", 188);
    add_key("minus", 189);
    add_key("period", 190);
    add_key("slash", 191);
    add_key("semicolon", 186);
    add_key("equal", 187);
    add_key("left_bracket", 219);
    add_key("backslash", 220);
    add_key("right_bracket", 221);
    add_key("graveaccent", 192);
    add_key("capslock", 20);
    add_key("scrolllock", 145);
    add_key("numlock", 144);
    add_key("printscreen", 44);
    add_key("pause", 19);
    add_key("keypad_0", 96);
    add_key("keypad_1", 97);
    add_key("keypad_2", 98);
    add_key("keypad_3", 99);
    add_key("keypad_4", 100);
    add_key("keypad_5", 101);
    add_key("keypad_6", 102);
    add_key("keypad_7", 103);
    add_key("keypad_8", 104);
    add_key("keypad_9", 105);
    add_key("keypad_decimal", 110);
    add_key("keypad_divide", 111);
    add_key("keypad_multiply", 106);
    add_key("keypad_subtract", 109);
    add_key("keypad_add", 107);
    add_key("keypad_enter", 269);
    add_key("left_shift", 160);
    add_key("left_ctrl", 162);
    add_key("left_alt", 164);
    add_key("left_super", 91);
    add_key("right_shift", 161);
    add_key("right_ctrl", 163);
    add_key("right_alt", 165);
    add_key("right_super", 92);
    add_key("menu", 93);
    add_key("0", 48);
    add_key("1", 49);
    add_key("2", 50);
    add_key("3", 51);
    add_key("4", 52);
    add_key("5", 53);
    add_key("6", 54);
    add_key("7", 55);
    add_key("8", 56);
    add_key("9", 57);
    add_key("a", 65);
    add_key("b", 66);
    add_key("c", 67);
    add_key("d", 68);
    add_key("e", 69);
    add_key("f", 70);
    add_key("g", 71);
    add_key("h", 72);
    add_key("i", 73);
    add_key("j", 74);
    add_key("k", 75);
    add_key("l", 76);
    add_key("m", 77);
    add_key("n", 78);
    add_key("o", 79);
    add_key("p", 80);
    add_key("q", 81);
    add_key("r", 82);
    add_key("s", 83);
    add_key("t", 84);
    add_key("u", 85);
    add_key("v", 86);
    add_key("w", 87);
    add_key("x", 88);
    add_key("y", 89);
    add_key("z", 90);
    add_key("f1", 112);
    add_key("f2", 113);
    add_key("f3", 114);
    add_key("f4", 115);
    add_key("f5", 116);
    add_key("f6", 117);
    add_key("f7", 118);
    add_key("f8", 119);
    add_key("f9", 120);
    add_key("f10", 121);
    add_key("f11", 122);
    add_key("f12", 123);

    Py_INCREF(keys);
    PyModule_AddObject(module, "keys", keys);

    Py_INCREF(Py_None);
    PyModule_AddObject(module, "wnd", Py_None);
    return module;
}
