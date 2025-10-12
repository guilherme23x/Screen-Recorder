import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import os
import datetime
import signal

class ScreenRecorder(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gravador de Tela")
        self.set_border_width(15)
        self.set_default_size(450, 300)
        self.set_resizable(False)
        self.connect("destroy", self.on_destroy)

        self.is_recording = False
        self.ffmpeg_process = None
        self.output_file = None
        self.capture_mode = "Screen"
        
        self.config_path = os.path.expanduser("~/.config/py_screen_recorder/config.txt")
        self.save_path = os.path.expanduser("~/Vídeos")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # --- Seção de Captura ---
        area_label = Gtk.Label(label="Área de Captura")
        area_label.set_halign(Gtk.Align.START)
        vbox.pack_start(area_label, False, False, 0)
        
        area_box = Gtk.Box(spacing=6)
        area_box.get_style_context().add_class("linked")
        
        screen_button = Gtk.RadioButton.new_with_label_from_widget(None, "Tela Inteira")
        screen_button.connect("toggled", self.on_mode_toggled, "Screen")
        window_button = Gtk.RadioButton.new_with_label_from_widget(screen_button, "Janela")
        window_button.connect("toggled", self.on_mode_toggled, "Window")
        selection_button = Gtk.RadioButton.new_with_label_from_widget(screen_button, "Seleção")
        selection_button.connect("toggled", self.on_mode_toggled, "Selection")
        
        area_box.pack_start(screen_button, True, True, 0)
        area_box.pack_start(window_button, True, True, 0)
        area_box.pack_start(selection_button, True, True, 0)
        vbox.pack_start(area_box, False, False, 5)

        # --- Seção de Áudio ---
        audio_label = Gtk.Label(label="Áudio")
        audio_label.set_halign(Gtk.Align.START)
        vbox.pack_start(audio_label, False, False, 0)
        self.audio_combo = Gtk.ComboBoxText()
        self.audio_combo.append_text("Com Áudio")
        self.audio_combo.append_text("Sem Áudio")
        self.audio_combo.set_active(0)
        vbox.pack_start(self.audio_combo, False, False, 5)

        # --- Seção de Destino ---
        dest_label = Gtk.Label(label="Pasta de Destino")
        dest_label.set_halign(Gtk.Align.START)
        vbox.pack_start(dest_label, False, False, 0)
        dest_box = Gtk.Box(spacing=6)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_hexpand(True)
        self.path_entry.set_editable(False)
        dest_box.pack_start(self.path_entry, True, True, 0)
        select_button = Gtk.Button(label="Selecionar...")
        select_button.connect("clicked", self.on_select_folder_clicked)
        dest_box.pack_start(select_button, False, False, 0)
        vbox.pack_start(dest_box, False, False, 5)

        # --- Botão de Gravação ---
        self.record_button = Gtk.Button(label="Gravar")
        self.record_button.get_style_context().add_class("suggested-action")
        self.record_button.connect("clicked", self.on_record_button_clicked)
        vbox.pack_end(self.record_button, False, False, 0)

        self.load_config()

    def load_config(self):
        config_dir = os.path.dirname(self.config_path)
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                path = f.read().strip()
                if path and os.path.isdir(path):
                    self.save_path = path
        else:
            os.makedirs(config_dir, exist_ok=True)
        self.path_entry.set_text(self.save_path)

    def save_config(self):
        config_dir = os.path.dirname(self.config_path)
        os.makedirs(config_dir, exist_ok=True)
        with open(self.config_path, 'w') as f:
            f.write(self.save_path)

    def on_select_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Selecione uma pasta para salvar os vídeos",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons("Cancelar", Gtk.ResponseType.CANCEL, "Selecionar", Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.save_path = dialog.get_filename()
            self.path_entry.set_text(self.save_path)
            self.save_config()
        dialog.destroy()

    def get_internal_audio_source(self):
        try:
            default_sink = subprocess.check_output(['pactl', 'get-default-sink'], text=True).strip()
            return f"{default_sink}.monitor"
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"Aviso: Não foi possível encontrar a fonte de áudio interna. {e}")
            return None

    def get_default_mic_source(self):
        try:
            return subprocess.check_output(['pactl', 'get-default-source'], text=True).strip()
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"Aviso: Não foi possível obter o microfone padrão. Usando 'default' como fallback. Erro: {e}")
            return 'default'
            
    def on_mode_toggled(self, button, name):
        if button.get_active():
            self.capture_mode = name

    def on_record_button_clicked(self, widget):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def get_geometry(self):
        self.hide()
        GLib.timeout_add(500, self._get_geometry_delayed)

    def _get_geometry_delayed(self):
        geometry_args = None
        try:
            if self.capture_mode == "Window":
                output = subprocess.check_output(['xdotool', 'selectwindow', 'getwindowgeometry']).decode('utf-8')
                lines = output.split('\n')
                pos_line = next(l for l in lines if 'Position' in l)
                geo_line = next(l for l in lines if 'Geometry' in l)
                pos_x, pos_y = pos_line.split(':')[1].strip().split(' ')[0].split(',')
                width, height = geo_line.split(':')[1].strip().split('x')
                geometry_args = f"-video_size {width}x{height} -i :0.0+{pos_x},{pos_y}"
            elif self.capture_mode == "Selection":
                output = subprocess.check_output(['slop', '-f', '%w %h %x %y']).decode('utf-8').strip()
                width, height, pos_x, pos_y = output.split(' ')
                geometry_args = f"-video_size {width}x{height} -i :0.0+{pos_x},{pos_y}"
        except (FileNotFoundError, subprocess.CalledProcessError, StopIteration, ValueError):
            dialog = Gtk.MessageDialog(
                transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK, text="Erro na Seleção",
            )
            dialog.format_secondary_text(f"Seleção cancelada ou falhou.\nVerifique se 'xdotool' e 'slop' estão instalados.")
            dialog.run()
            dialog.destroy()
        finally:
            self.show()

        if geometry_args:
            self.execute_ffmpeg(geometry_args.split())
        elif self.capture_mode == "Screen":
            self.execute_ffmpeg(["-i", ":0.0"])
        else:
             self.reset_button()

    def start_recording(self):
        self.record_button.set_sensitive(False)
        self.get_geometry()
        
    def execute_ffmpeg(self, video_input_args):
        if not video_input_args:
            self.reset_button()
            return
            
        self.is_recording = True
        self.record_button.set_label("Parar Gravação")
        self.record_button.get_style_context().set_state(Gtk.StateFlags.ACTIVE)
        self.record_button.set_sensitive(True)
        
        framerate = "60"
        audio_choice = self.audio_combo.get_active_text()
        
        command = ['ffmpeg', '-y', '-thread_queue_size', '1024', '-framerate', framerate, '-f', 'x11grab', *video_input_args]
        audio_input_part = []
        codec_and_filter_part = ['-c:v', 'libx264', '-preset', 'ultrafast', '-qp', '0']

        if audio_choice == "Com Áudio":
            internal_source = self.get_internal_audio_source()
            mic_source = self.get_default_mic_source()
            if internal_source and mic_source:
                audio_input_part.extend(['-f', 'pulse', '-i', internal_source])
                audio_input_part.extend(['-f', 'pulse', '-i', mic_source])
                codec_and_filter_part.extend([
                    '-filter_complex', '[1:a][2:a]amix=inputs=2:duration=longest[a]',
                    '-map', '0:v', '-map', '[a]', '-ac', '2'
                ])
            else:
                print("Aviso: Uma das fontes de áudio não foi encontrada. Gravando sem áudio.")
                codec_and_filter_part.append('-an')
        else: 
            codec_and_filter_part.append('-an')
            
        command.extend(audio_input_part)
        command.extend(codec_and_filter_part)

        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Gravação_{time_str}.mp4"
        self.output_file = os.path.join(self.save_path, filename)
        os.makedirs(self.save_path, exist_ok=True)
        command.append(self.output_file)
        
        print("\nComando FFmpeg executado:")
        print(" ".join(command) + "\n")
        
        self.ffmpeg_process = subprocess.Popen(command)

    def stop_recording(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.send_signal(signal.SIGINT)
            self.ffmpeg_process.wait()
            self.ffmpeg_process = None
            print(f"Gravação finalizada. Vídeo salvo em: {self.output_file}")
        
        self.is_recording = False
        self.reset_button()

    def reset_button(self):
        self.record_button.set_label("Gravar")
        self.record_button.get_style_context().set_state(Gtk.StateFlags.NORMAL)
        self.record_button.set_sensitive(True)

    def on_destroy(self, *args):
        if self.is_recording:
            self.stop_recording()
        Gtk.main_quit()

if __name__ == "__main__":
    win = ScreenRecorder()
    win.show_all()
    Gtk.main()

