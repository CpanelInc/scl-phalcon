OBS_PROJECT := EA4
scl-php71-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8
scl-php70-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8
scl-php56-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8
scl-php55-php-phalcon-obs : DISABLE_BUILD += repository=CentOS_8
include $(EATOOLS_BUILD_DIR)obs-scl.mk
