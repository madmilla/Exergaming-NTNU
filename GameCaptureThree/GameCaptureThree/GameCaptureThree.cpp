// GameCaptureThree.cpp : Defines the entry point for the application.
//
#include "stdafx.h"
#include <stdio.h>
#include "GameCaptureThree.h"
#include <sys/timeb.h>

int getMilliCount() {
	timeb tb;
	ftime(&tb);
	int nCount = tb.millitm + (tb.time & 0xfffff) * 1000;
	return nCount;
}

int getMilliSpan(int nTimeStart) {
	int nSpan = getMilliCount() - nTimeStart;
	if (nSpan < 0)
		nSpan += 0x100000 * 1000;
	return nSpan;
}

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE hInst;                                // current instance
WCHAR szTitle[MAX_LOADSTRING];                  // The title bar text
WCHAR szWindowClass[MAX_LOADSTRING];            // the main window class name
int i;
char c[100];
char buffer[5];



// Forward declarations of functions included in this code module:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // TODO: Place code here.
	MSG msg;
	//HACCEL hAccelTable;

	// CODE BLOCK LARS UP HERE

    // Initialize global strings
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_GAMECAPTURETHREE, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // Perform application initialization:
    if (!InitInstance (hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_GAMECAPTURETHREE));

    // Main message loop:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int) msg.wParam;
}



//
//  FUNCTION: MyRegisterClass()
//
//  PURPOSE: Registers the window class.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style          = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = WndProc;
    wcex.cbClsExtra     = 0;
    wcex.cbWndExtra     = 0;
    wcex.hInstance      = hInstance;
    wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_GAMECAPTURETHREE));
    wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName   = MAKEINTRESOURCEW(IDC_GAMECAPTURETHREE);
    wcex.lpszClassName  = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   FUNCTION: InitInstance(HINSTANCE, int)
//
//   PURPOSE: Saves instance handle and creates main window
//
//   COMMENTS:
//
//        In this function, we save the instance handle in a global variable and
//        create and display the main program window.
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // Store instance handle in our global variable

   HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

   if (!hWnd)
   {
      return FALSE;
   }

   ShowWindow(hWnd, 6);//nCmdShow
   UpdateWindow(hWnd);
  
   return TRUE;
}

//	FUNCTION:	CaptureAnImage
//	Purpose:	Capture a screenshot into a window and then save it to a BMP
//	Comments:	i hope this shit works

void GetDesktopResolution(int& horizontal, int& vertical)
{
	RECT desktop;
	// Get a handle to the desktop window
	const HWND hDesktop = GetDesktopWindow();
	// Get the size of screen to the variable desktop
	GetWindowRect(hDesktop, &desktop);
	// The top left corner will have coordinates (0,0)
	// and the bottom right corner will have coordinates
	// (horizontal, vertical)
	horizontal = desktop.right;
	vertical = desktop.bottom;
}

int CaptureAnImage(HWND hWnd)
{
	HDC hdcScreen;
	HDC hdcWindow;
	HDC hdcMemDC = NULL;
	HBITMAP hbmScreen = NULL;
	BITMAP bmpScreen;
	int horizontal = 0;
	int vertical = 0;
	GetDesktopResolution(horizontal, vertical);

	//	Retrieve the fucking handle to a display device context for the client.
	//	Area of the window
	hdcScreen = GetDC(NULL);
	hdcWindow = GetDC(NULL);

	//	Create a compatible DC which is used in a bitbit from the window DC
	hdcMemDC = CreateCompatibleDC(hdcWindow);

	if (!hdcMemDC) {
		MessageBox(hWnd, "CreatecompatibleDC had Failed", "Failed", MB_OK);
		goto done;
	}

	//	Get the client area for size calculation
	RECT rcClient;
	// Get the size of screen to the variable desktop
	GetWindowRect(hWnd, &rcClient);
	//GetClientRect(hWnd, &rcClient);

	//	This is the best stretch mode
	SetStretchBltMode(hdcWindow, HALFTONE);

	//	The source DC is the entrie screen and the destination DC is the current window(HWND)
	if (!StretchBlt(hdcWindow, 
		0, 0, 
		horizontal,
		vertical, 
		hdcScreen, 
		0, 0, 
		GetSystemMetrics(SM_CXSCREEN), 
		GetSystemMetrics(SM_CYSCREEN), 
		SRCCOPY)) {
		MessageBox(hWnd, "StretchBlt has failed", "failed", MB_OK);
		goto done;
	}

	//	Create a compatible bitmap from the window DC
	hbmScreen = CreateCompatibleBitmap(hdcWindow, 
		horizontal,
		vertical);

	if (!hbmScreen) {
		MessageBox(hWnd, "CreateCompatibleBitmap has failed", "Failed", MB_OK);
		goto done;
	}

	// Select the compatible bitmap into the compatible memory DC
	SelectObject(hdcMemDC, hbmScreen);

	// Bit block transfer into our compatible memory DC/
	if (!BitBlt(hdcMemDC, 
		0, 0, 
		horizontal,
		vertical,
		hdcWindow, 
		0, 0, 
		SRCCOPY)) {
		MessageBox(hWnd, "BitBlt has failed", "Failed",MB_OK);
		goto done;
	}

	// Get the BITMAP from the HBITMAP
	GetObject(hbmScreen, sizeof(BITMAP), &bmpScreen);

	BITMAPFILEHEADER bmfHeader;
	BITMAPINFOHEADER bi;

	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = bmpScreen.bmWidth;
	bi.biHeight = bmpScreen.bmHeight;
	bi.biPlanes = 1;
	bi.biBitCount = 32; // was 32
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrUsed = 0;
	bi.biClrImportant = 0;

	DWORD dwBmpSize = ((bmpScreen.bmWidth * bi.biBitCount + 31) / 32) * 4 * bmpScreen.bmHeight;
	//DWORD dwBmpSize = bmpScreen.bmWidth * abs(bmpScreen.bmHeight)*(bi.biBitCount + 7) / 8;
	HANDLE hDIB = GlobalAlloc(GHND, dwBmpSize);
	char *lpbitmap = (char *)GlobalLock(hDIB);

	//Gets the bits from the bitmap and copies them into a buffer which is pointed to by lpbitmpa
	GetDIBits(hdcWindow, hbmScreen, 0, (UINT)bmpScreen.bmHeight, lpbitmap, (BITMAPINFO *)&bi, DIB_RGB_COLORS);

	// a file is created this is where we will save the screen capture
	strcpy_s(c, "C:\\LarsTest\\spel_");
	sprintf_s(buffer, "%d", i);
	strcat_s(c, buffer);
	strcat_s(c, ".bmp");
	
	HANDLE hFILE = CreateFile(c, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	i++;
	// Add the size of the headers to the size of the bitmap to get the total file size
	DWORD dwSizeOfDIB = dwBmpSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

	// offset to where the actual bitmap bits start
	bmfHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);

	// size of the file
	bmfHeader.bfSize = dwSizeOfDIB;

	// bfType must always be BM for Bitmaps
	bmfHeader.bfType = 'MB'; // BM

	DWORD dwBytesWritten = 0;
	WriteFile(hFILE, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
	WriteFile(hFILE, (LPSTR)&bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
	WriteFile(hFILE, (LPSTR)lpbitmap, dwBmpSize, &dwBytesWritten, NULL);
	//	Unlock & FREE DIB from the heap
	GlobalUnlock(hDIB);
	GlobalFree(hDIB);

	// Close the handle for the file that was created
	CloseHandle(hFILE);

	//	Clean up
done:
	DeleteObject(hbmScreen);
	DeleteObject(hdcMemDC);
	ReleaseDC(NULL, hdcScreen);
	ReleaseDC(hWnd, hdcWindow);
	
	return 0;
}

//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE:  Processes messages for the main window.
//
//  WM_COMMAND  - process the application menu
//  WM_PAINT    - Paint the main window
//  WM_DESTROY  - post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	i = 1;
	PAINTSTRUCT ps;
    switch (message)
    {
	case WM_CREATE:
	{
		break;
	}
    case WM_COMMAND:
        {
            int wmId = LOWORD(wParam);
            // Parse the menu selections:
            switch (wmId)
            {
            case IDM_ABOUT:
                DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
                break;
            case IDM_EXIT:
                DestroyWindow(hWnd);
                break;
            default:
                return DefWindowProc(hWnd, message, wParam, lParam);
            }
        }
        break;
	case WM_MOVE:
    case WM_PAINT:
        {
            //HDC hdc = BeginPaint(hWnd, &ps);
			//CaptureAnImage(hWnd);
		
           // EndPaint(hWnd, &ps);
			int n, start, milliSecondsElapsed = 0;
			while (true) {
				start = getMilliCount();
				CaptureAnImage(hWnd);
				//milliSecondsElapsed = getMilliSpan(start);
				if ((200 - getMilliSpan(start)) < 0) { continue;  }
				Sleep(200 - getMilliSpan(start));


				//end = clock() - start;//this will give you time spent between those two calls.
				//strcpy_s(c, "difference in seconds");
				//sprintf_s(buffer, "%f", end);
				//strcat_s(c, buffer);
				//strcat_s(c, " something");

				//std::cerr << end << std::endl;
				//std::cerr << "\n" << std::endl;
				//OutputDebugString(end);
				
				//if (milliSecondsElapsed > 200) {
					//continue;
				//}
							}
			//MessageBox(hWnd, L"Succes", L"Failed", MB_OK);
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
		//HDC hdc = BeginPaint(hWnd, &ps);
		//CaptureAnImage(hWnd);
		//EndPaint(hWnd, &ps);
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}
