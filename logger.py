import logging
import os
from datetime import datetime
import yaml
from logging.handlers import TimedRotatingFileHandler

# グローバルロガーインスタンスを初期化します。
logger = logging.getLogger('aina_ytloop')

def setup_logging(settings):
    """
    ロギング設定を初期化します。
    config.yamlから設定を読み込み、コンソールとファイルへのログ出力を設定します。
    """
    log_settings = settings.get('logging', {})

    # ロガーにハンドラが複数追加されるのを防ぎます。
    if logger.handlers:
        return

    log_dir = log_settings.get('log_directory', 'logs')
    # ログディレクトリが存在しない場合は作成します。
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_level_str = log_settings.get('level', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    # フォーマッターを作成します。
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # コンソールハンドラーを設定します。
    if log_settings.get('log_to_console', True):
        c_handler = logging.StreamHandler()
        c_handler.setLevel(log_level)
        c_handler.setFormatter(formatter)
        logger.addHandler(c_handler)

    # ファイルハンドラーを設定します。
    if log_settings.get('log_to_file', True):
        rotation_settings = log_settings.get('rotation', {})
        
        if rotation_settings.get('enabled', False):
            # ログローテーションが有効な場合
            log_filepath = os.path.join(log_dir, 'app.log')
            f_handler = TimedRotatingFileHandler(
                log_filepath,
                when=rotation_settings.get('when', 'D'),
                interval=rotation_settings.get('interval', 1),
                backupCount=rotation_settings.get('backup_count', 30),
                encoding='utf-8'
            )
            logger.info("ログローテーションを有効にしてファイルハンドラーを設定しました。")
        else:
            # ログローテーションが無効な場合 (従来通り)
            log_file_name_timestamp_format = log_settings.get('log_file_name_timestamp_format', '%Y%m%d_%H%M%S')
            log_filename = datetime.now().strftime(f"app_{log_file_name_timestamp_format}.log")
            log_filepath = os.path.join(log_dir, log_filename)
            f_handler = logging.FileHandler(log_filepath, encoding='utf-8')
            logger.info("タイムスタンプ付きログファイルハンドラーを設定しました。")

        f_handler.setLevel(log_level)
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)