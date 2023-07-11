OBS_PROJECT := EA4
scl-php73-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_9
scl-php72-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_9
scl-php71-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php70-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php56-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php55-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
include $(EATOOLS_BUILD_DIR)obs-scl.mk
