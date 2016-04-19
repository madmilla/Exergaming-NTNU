using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Kinect;
using System.Threading;
using System.IO;

namespace Theia
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        KinectSensor _sensor;
        MultiSourceFrameReader _reader;
        Mode _mode = Mode.Color;

        public MainWindow()
        {
            _sensor = KinectSensor.GetDefault();
            if (_sensor != null)
            {
                _sensor.Open();
                _reader = _sensor.OpenMultiSourceFrameReader(FrameSourceTypes.Color | FrameSourceTypes.Depth | FrameSourceTypes.Infrared);
                _reader.MultiSourceFrameArrived += Reader_MultiSourceFrameArrived;
            }

            

          
            InitializeComponent();
        }

        void Reader_MultiSourceFrameArrived(object sender, MultiSourceFrameArrivedEventArgs e)
        {
            // Get a reference to the multiframe
            var reference = e.FrameReference.AcquireFrame();

            //COLOR
            using (var frame = reference.ColorFrameReference.AcquireFrame())
            {
                if (frame != null && _mode == Mode.Color)
                {
                    camera.Source = ToBitmap(frame);
                }
            }
            //DEPTH
            using (var frame = reference.DepthFrameReference.AcquireFrame())
            {
                if (frame != null && _mode == Mode.Depth )
                {
                    camera.Source = ToBitmap(frame);
                }
            }
            //INFRARED
            using (var frame = reference.InfraredFrameReference.AcquireFrame())
            {
                if(frame != null && _mode == Mode.Infrared)
                {
                    camera.Source = ToBitmap(frame);
                }
            }
    
        }

        private ImageSource ToBitmap(ColorFrame frame)
        {
            int width = frame.FrameDescription.Width;
            int height = frame.FrameDescription.Height;
            PixelFormat format = PixelFormats.Bgr32;

            byte[] pixels = new byte[width * height * ((format.BitsPerPixel + 7) / 8)];

            if (frame.RawColorImageFormat == ColorImageFormat.Bgra)
            {
                frame.CopyRawFrameDataToArray(pixels);
            }
            else
            {
                frame.CopyConvertedFrameDataToArray(pixels, ColorImageFormat.Bgra);
            }

            int stride = width * format.BitsPerPixel / 8;

            return BitmapSource.Create(width, height, 96,96, format, null, pixels, stride);
        }

        private ImageSource ToBitmap(DepthFrame frame)
        {
            int width = frame.FrameDescription.Width;
            int height = frame.FrameDescription.Height;
            PixelFormat format = PixelFormats.Bgr32;

            ushort minDepth = frame.DepthMinReliableDistance;
            ushort maxDepth = frame.DepthMaxReliableDistance;

            ushort[] depthData = new ushort[width * height];
            byte[] pixelData = new byte[width * height * (format.BitsPerPixel + 7) / 8];

            frame.CopyFrameDataToArray(depthData);

            int colorIndex = 0;

            for (int depthIndex = 0; depthIndex < depthData.Length; ++depthIndex)
            {
                ushort depth = depthData[depthIndex];
                byte intensity = (byte)(depth >= minDepth && depth <= maxDepth ? depth : 0);

                pixelData[colorIndex++] = intensity; //BLUE
                pixelData[colorIndex++] = intensity; //GREEN
                pixelData[colorIndex++] = intensity; //RED

                ++colorIndex;
            }

            int stride = width * format.BitsPerPixel / 8;
            return BitmapSource.Create(width, height, 96, 96, format, null, pixelData, stride);
             
        }

        private ImageSource ToBitmap(InfraredFrame frame)
        {
            int width = frame.FrameDescription.Width;
            int height = frame.FrameDescription.Height;
            PixelFormat format = PixelFormats.Bgr32;

            ushort[] infraredData = new ushort[width * height];
            byte[] pixelData = new byte[width * height * (format.BitsPerPixel + 7) / 8];

            frame.CopyFrameDataToArray(infraredData);

            int colorIndex = 0;
            for (int infraredIndex = 0; infraredIndex < infraredData.Length; ++infraredIndex)
            {
                ushort ir = infraredData[infraredIndex];
                byte intensity = (byte)(ir >> 8);

               /* pixelData[colorIndex++] = (byte)(intensity / 1); //BLUE
                pixelData[colorIndex++] = (byte)(intensity / 1); //GREEN
                pixelData[colorIndex++] = (byte)(intensity / 0.4); //RED*/
                pixelData[colorIndex++] = intensity; //BLUE
                pixelData[colorIndex++] = intensity; //GREEN
                pixelData[colorIndex++] = intensity; //RED
                ++colorIndex;
            }

            int stride = width * format.BitsPerPixel / 8;
            return BitmapSource.Create(width, height, 96, 96, format, null, pixelData, stride);

        }

        private void Color_mode(object sender, RoutedEventArgs e)
        {
            _mode = Mode.Color;
        }

        private void Depth_mode(object sender, RoutedEventArgs e)
        {
            _mode = Mode.Depth;
        }

        private void Infrared_mode(object sender, RoutedEventArgs e)
        {
            _mode = Mode.Infrared;
        }

        public enum Mode
        {
            Color,
            Depth,
            Infrared
        }
    }
}
