Q=@
CDL_REGRESS = ${CDL_ROOT}/libexec/cdl/cdl_regress.py

SMOKE_OPTIONS = --only-tests 'smoke'
SMOKE_TESTS   = test_prng_entropy test_apb_target_prng
REGRESS_TESTS = test_prng_entropy test_apb_target_prng
CDL_REGRESS_PACKAGE_DIRS = --package-dir regress:${SRC_ROOT}/python  --package-dir regress:${GRIP_ROOT_PATH}/atcf_hardware_apb/python --package-dir regress:${GRIP_ROOT_PATH}/atcf_hardware_utils/python

.PHONY:smoke
smoke:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} ${CDL_REGRESS_PACKAGE_DIRS} --suite-dir=python ${SMOKE_OPTIONS} ${SMOKE_TESTS}

.PHONY:regress
regress:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} ${CDL_REGRESS_PACKAGE_DIRS} --suite-dir=python ${REGRESS_TESTS}

create_entropy:
	PYTHONPATH=${PYTHONPATH}:${GRIP_ROOT_PATH}/atcf_hardware_utils/python python3 ${GRIP_ROOT_PATH}/atcf_hardware_crypto/python/crypto/prng.py

ASSESS_FILE=${GRIP_ROOT_PATH}/atcf_hardware_crypto/one_per_four_32
ASSESS_FILE=/Users/gavinprivate/sts-2.1.2/data/data.pi
ASSESS_IS_01=0
ASSESS_FILE=${GRIP_ROOT_PATH}/atcf_hardware_crypto/one_per_sixteen_32
ASSESS_IS_01=1
ASSESS_FILE=/Users/gavinprivate/sts-2.1.2/data/data.bad_rng
ASSESS_IS_01=1
assess_entropy:
	# For universal you need a long streams - run with >150000
	# for random excursions you need shorter streams - run with 10000
	# (cd ~/sts-2.1.2 && 	printf "0\n${ASSESS_FILE}\n1\n0\n40\n${ASSESS_IS_01}\n" | ./assess 25000)
	# (cd ~/sts-2.1.2 && 	printf "0\n${ASSESS_FILE}\n1\n0\n10\n${ASSESS_IS_01}\n" | ./assess 100000)
	# (cd ~/sts-2.1.2 && 	printf "0\n${ASSESS_FILE}\n1\n0\n8\n${ASSESS_IS_01}\n" | ./assess 120000)
	# (cd ~/sts-2.1.2 && 	printf "0\n${ASSESS_FILE}\n1\n0\n3\n${ASSESS_IS_01}\n" | ./assess 300000)
	(cd ~/sts-2.1.2 && 	printf "0\n${ASSESS_FILE}\n1\n0\n1\n${ASSESS_IS_01}\n" | ./assess 1000000)

