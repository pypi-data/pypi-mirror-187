/*
	This is a file improve move window function and add some long value to change the window.
	Use function : "SetWindowLong" to change window's attribute.
	Include : windows.h
	Compile with : mw.def
	__declspec(dllexport) HWND gethwnd() {
		<Get target window's hwnd and set it>
		no args
		hwnd = findwindow("...")
	}
	__declspec(dllexport) void moving(int x, int y, int eventx, int eventy) {
		<move window's funcition>
		x, y, eventx, eventy : int
		"x : windowx | y : windowy | eventx : mousex | eventy : mousey"
	}
	__declspec(dllexport) void setwindowlong() {
		<To change the window's attribute>
		no args
	}
*/
#include <windows.h>
#pragma comment(lib, "user32.lib")

__declspec(dllexport) inline void move(HWND hwnd, int x, int y, int eventx, int eventy) { SetWindowPos(hwnd, NULL, eventx + x, eventy + y, 0, 0, SWP_NOREDRAW | SWP_NOSIZE | SWP_SHOWWINDOW); } // x : windowx | y : windowy | eventx : mousex | eventy : mousey

__declspec(dllexport) void setwindow(HWND hwnd) { // Find the hwnd of the window : call only once
	SetWindowLong(hwnd, GWL_EXSTYLE, WS_EX_APPWINDOW); // What I improved in 1.0.5.6
	SetWindowLong(hwnd, GWL_STYLE, WS_VISIBLE | WS_THICKFRAME); // What I improvoed in 1.0.5.5
}
