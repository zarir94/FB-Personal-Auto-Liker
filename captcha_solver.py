import os, requests, ffmpeg_downloader as ffdl, whisper, warnings, shutil

warnings.filterwarnings("ignore")

class FFMPEG_Path_Error(Exception): pass
class Block_Error(Exception): pass
class Recaptcha_Not_Found(Exception): pass

class Recaptcha_Solver:
    """### Usage
	solver = Recaptcha_Solver(page, ffmpeg_path, log)\n
	solver.solve_recaptcha()

    ### Params
    page: DrissionPage.ChromiumPage
        This param is required.

    ffmpeg_path: str
        This param is optional. Provide ffmpeg executable `file` path
        or the `folder` path where ffmpeg exists.
        If nothing provided, it will use the ffmpeg from system.
        If ffmpeg is not found in your system, it will automaticlly download and install it.

    log: bool
        Set True if you want to view the progress.
	"""
    def __init__(s, page, ffmpeg_path:str = None, log:bool = False, exit_before_exception:bool = False) -> None:
        s.m = whisper.load_model("base.en")
        s.ebe = exit_before_exception
        s.p = page
        s.f = s.p.get_frame('css:iframe[title="reCAPTCHA"]')
        if not s.f:
            if s.ebe:
                s.p.quit()
            raise Recaptcha_Not_Found('Seems like recaptcha is not present in the current page.')
        s.fp = ffmpeg_path
        s.l = log
        s.manage_ffmpeg()
    
    def manage_ffmpeg(s):
        if not s.fp:
            s.fp=shutil.which('ffmpeg')
            if not s.fp:
                if not ffdl.installed():
                    os.system('ffdl install --add-path -y')
                s.fp = ffdl.ffmpeg_path

        if not os.path.exists(s.fp):
            if s.ebe:
                s.p.quit()
            raise FFMPEG_Path_Error('The ffmpeg path does not exists. Path: %s' % s.fp)

        if os.path.isfile(s.fp):
            s.fp = os.path.dirname(s.fp)

        os.environ['PATH'] = os.pathsep.join([os.environ.get("PATH", ''), str(s.fp)])
    
    def o(s,*a,**b):
        b['end'], b['sep'] = '', ' '
        if s.l: print('\r' + b['sep'].join(a), **b)
    
    def transcribe(s, url):
        with open('.temp', 'wb') as f:
            s.o('Downloading Audio...')
            f.write(requests.get(url).content)
        s.o('Transcribing Audio...')
        try:
            result = s.m.transcribe('.temp')
        except FileNotFoundError:
            if s.ebe:
                s.p.quit()
            raise FileNotFoundError('FFMPEG executable is not found.')
        os.remove('.temp')
        return result["text"].strip()

    def click_checkbox(s):
        s.o('Clicking Checkbox...')
        s.f.ele('css:#recaptcha-anchor-label').click()

    def request_audio_version(s):
        s.o('Switching to Audio...')
        s.f2 = s.p.get_frame("xpath:.//iframe[@title='recaptcha challenge expires in two minutes']")
        s.f2.ele('css:#recaptcha-audio-button').click()

    def solve_audio_captcha(s):
        text = s.transcribe(s.f2.ele('css:#audio-source').attr('src'))
        s.o('Sending transcribe...')
        s.f2.ele('css:#audio-response').input(text)
        s.f2.ele('css:#recaptcha-verify-button').click()

    def check_blocking(s):
        if s.f2.ele('css:.rc-doscaptcha-header-text'):
            if s.ebe:
                s.p.quit()
            raise Block_Error('Request blocked by google.')

    def solve_recaptcha(s):
        s.click_checkbox()
        try:
            s.request_audio_version()
            s.solve_audio_captcha()
        except KeyboardInterrupt:
            if s.ebe:
                s.p.quit()
            raise KeyboardInterrupt
        except:
            s.check_blocking()

        s.o('Recaptcha Solved\n')


if __name__ == '__main__':
    from DrissionPage import ChromiumPage
    import psutil, time
    page = ChromiumPage()
    page.quit = lambda: [proc.kill() for proc in psutil.process_iter() if proc.name().__contains__('chrome')]
    page.get('https://www.google.com/recaptcha/api2/demo')
    Recaptcha_Solver(page).solve_recaptcha()
    time.sleep(10)
    page.quit()

