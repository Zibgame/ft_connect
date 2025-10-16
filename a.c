// altf4_x11.c
// Compile with: gcc altf4_x11.c -o altf4_x11 -lX11 -lXtst

#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <X11/extensions/XTest.h>
#include <stdio.h>
#include <unistd.h>

int main(void) {
    Display *dpy = XOpenDisplay(NULL);
	int i = 10;
    if (!dpy) {
        return 1;
    }

    // Get keycodes for Alt and F4
    KeyCode alt = XKeysymToKeycode(dpy, XK_Alt_L);
    KeyCode f4  = XKeysymToKeycode(dpy, XK_F4);
	KeyCode enter = XKeysymToKeycode(dpy, XK_Return);

	while (i > 0)
	{
		// Press Alt
		XTestFakeKeyEvent(dpy, alt, True, CurrentTime);
		XFlush(dpy);
		// Press F4
		XTestFakeKeyEvent(dpy, f4, True, CurrentTime);
		XFlush(dpy);

		// Release F4 then Alt
		XTestFakeKeyEvent(dpy, f4, False, CurrentTime);
		XFlush(dpy);
		XTestFakeKeyEvent(dpy, alt, False, CurrentTime);
		XFlush(dpy);


		XTestFakeKeyEvent(dpy, enter, True, CurrentTime);   // key down
		XFlush(dpy);
		XTestFakeKeyEvent(dpy, enter, False, CurrentTime);  // key up
		XFlush(dpy);
		i--;
		sleep(10);
	}
		XCloseDisplay(dpy);
    return 0;
}

// ~/../../sgoinfre/goinfre/Perso/zcadinot/ft_connect/script/1.out