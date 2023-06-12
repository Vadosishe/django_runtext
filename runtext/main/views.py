import cv2
import pygame
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

from .forms import MyForm


class ScreenRecorder:
    def __init__(self, width, height, fps, out_file='output.avi'):
        four_cc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(out_file, four_cc, float(fps), (width, height))

    def capture_frame(self, surf):
        pixels = cv2.rotate(pygame.surfarray.pixels3d(surf), cv2.ROTATE_90_CLOCKWISE)
        pixels = cv2.flip(pixels, 1)
        pixels = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)
        self.video.write(pixels)

    def end_recording(self):
        # stop recording
        self.video.release()


def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            return HttpResponse('Форма отправлена')
    else:
        form = MyForm()
    return render(request, 'my_template.html', {'form': form})


def index(request):
    print(request.POST)
    return render(request, 'main/index.html')


def runtext(request):
    print(request.path.split("=")[1])
    return render(request, "main/runtext.html")


def about(request):
    return render(request, "main/about.html")


def documentation(request):
    return render(request, "main/docs.html")


def generate_video(request):
    inpt = request.path.split("=")[1]
    pygame.init()
    video_duration = 3
    FPS = 30
    screen_size = (100, 100)
    PURPLE = (128, 0, 128)
    WHITE = (255, 255, 255)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("cambria", 45)
    text = font.render(inpt, True, WHITE, PURPLE)
    recorder = ScreenRecorder(screen_size[0], screen_size[1], FPS)
    x, y = screen_size[0], screen_size[1] / 2 - text.get_height() / 2
    dx = (text.get_width() + screen_size[0] / 2) / (FPS * video_duration)
    count = 0
    total_frames = FPS * video_duration + 1
    while count < total_frames:
        clock.tick(FPS)
        screen.fill(PURPLE)
        screen.blit(text, (x, y))
        pygame.display.update()
        recorder.capture_frame(screen)
        x -= dx
        count += 1
    recorder.end_recording()


def download(request):
    generate_video(request.path.split("=")[1])
    file_path = r"C:\Users\Mi\PycharmProjects\django_runtext\runtext\output.avi"
    file_name = "output.avi"
    file = open(file_path, "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response
