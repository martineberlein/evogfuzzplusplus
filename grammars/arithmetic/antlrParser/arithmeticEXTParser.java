// Generated from ./antlrParser/arithmeticEXT.g4 by ANTLR 4.7.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class arithmeticEXTParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		Whitespace=25;
	public static final int
		RULE_main_dummy_rule_hope_for_no_collisions = 0, RULE_start = 1, RULE_exp = 2, 
		RULE_term = 3, RULE_factor = 4, RULE_digitrec = 5, RULE_digit = 6, RULE_bool = 7;
	public static final String[] ruleNames = {
		"main_dummy_rule_hope_for_no_collisions", "start", "exp", "term", "factor", 
		"digitrec", "digit", "bool"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'-'", "'+'", "'/'", "'*'", "'('", "')'", "'4'", "'5'", "'0'", "'1'", 
		"'3'", "'8'", "'7'", "'9'", "'6'", "'2'", "'f'", "'a'", "'l'", "'s'", 
		"'e'", "'n'", "'u'", "'true'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, "Whitespace"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "arithmeticEXT.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }


	double _25a67066_8c4d_4a6b_9eb7_57b187a6ef3b= 0.0;
	double _ed4c3af8_ba43_4abc_93a3_263acf446903= 0.0;
	double _84c9ec57_f716_4df2_9720_454d02974ba8= 0.0;
	double _16f8c1e5_f3e7_412e_8297_320510778a62= 0.0;
	double _0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c= 0.0;
	double _bfc12918_db0c_40bc_84df_98481fcb11ec= 0.0;
	double _cc82d6ad_25ed_460f_a9c9_d64bdc47586d= 0.0;
	double _cdd6587e_5c46_4048_bab1_3b75bb0daa4c= 0.0;
	double _58389b8d_df39_4f1b_b749_e6927ae792e4= 0.0;
	double _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b= 0.0;
	double _e91a1ede_82b9_4180_ada2_d5608aef67b5= 0.0;
	double _5d175fcf_7a7b_428f_96ad_205aba37c7e5= 0.0;
	double _8e079b6b_87a2_429b_b4be_820e1fc39507= 0.0;
	double _c07ca19a_b839_4480_83cc_35933bf57c6d= 0.0;
	double _15408aa6_088b_4b48_a7f0_04e8898cee35= 0.0;
	double _aca820eb_5a72_4941_b593_63d459e0180d= 0.0;
	double _cf60f941_8297_47e7_93d3_14a5d2cfb58a= 0.0;
	double _acc6bd49_041c_4dce_9a3d_eefa92b34e6d= 0.0;
	double _0debc092_3675_41e0_8b4a_425efd383094= 0.0;
	double _0e615a7b_f485_436f_9864_b3705e7b6a35= 0.0;
	double _1a682da2_5101_4388_8e2e_00900a51ff49= 0.0;
	double _3865f17e_d1ac_460c_b791_5e321bf40b8e= 0.0;
	double _3007af0c_d472_4b02_8dfe_6458ee4dd16b= 0.0;
	double _70bdf0f7_701f_46e2_a157_ba55bfad7772= 0.0;
	double _9e12b4ff_e74d_4097_9cb0_23746944f381= 0.0;
	double _943aa8c3_767e_44a6_9fa7_69de86eef832= 0.0;
	double _0b697d8c_00a4_4262_acb2_021ebe124eae= 0.0;
	double _prob_25a67066_8c4d_4a6b_9eb7_57b187a6ef3b= 0.0;
	double _prob_84c9ec57_f716_4df2_9720_454d02974ba8= 0.0;
	double _prob_16f8c1e5_f3e7_412e_8297_320510778a62= 0.0;
	double _prob_ed4c3af8_ba43_4abc_93a3_263acf446903= 0.0;
	double _prob_bfc12918_db0c_40bc_84df_98481fcb11ec= 0.0;
	double _prob_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c= 0.0;
	double _prob_cc82d6ad_25ed_460f_a9c9_d64bdc47586d= 0.0;
	double _prob_6e6682fc_4517_4b8b_ad5f_64461ba3ed7b= 0.0;
	double _prob_cdd6587e_5c46_4048_bab1_3b75bb0daa4c= 0.0;
	double _prob_58389b8d_df39_4f1b_b749_e6927ae792e4= 0.0;
	double _prob_e91a1ede_82b9_4180_ada2_d5608aef67b5= 0.0;
	double _prob_5d175fcf_7a7b_428f_96ad_205aba37c7e5= 0.0;
	double _prob_8e079b6b_87a2_429b_b4be_820e1fc39507= 0.0;
	double _prob_c07ca19a_b839_4480_83cc_35933bf57c6d= 0.0;
	double _prob_0e615a7b_f485_436f_9864_b3705e7b6a35= 0.0;
	double _prob_1a682da2_5101_4388_8e2e_00900a51ff49= 0.0;
	double _prob_3865f17e_d1ac_460c_b791_5e321bf40b8e= 0.0;
	double _prob_0debc092_3675_41e0_8b4a_425efd383094= 0.0;
	double _prob_3007af0c_d472_4b02_8dfe_6458ee4dd16b= 0.0;
	double _prob_cf60f941_8297_47e7_93d3_14a5d2cfb58a= 0.0;
	double _prob_15408aa6_088b_4b48_a7f0_04e8898cee35= 0.0;
	double _prob_acc6bd49_041c_4dce_9a3d_eefa92b34e6d= 0.0;
	double _prob_70bdf0f7_701f_46e2_a157_ba55bfad7772= 0.0;
	double _prob_aca820eb_5a72_4941_b593_63d459e0180d= 0.0;
	double _prob_0b697d8c_00a4_4262_acb2_021ebe124eae= 0.0;
	double _prob_9e12b4ff_e74d_4097_9cb0_23746944f381= 0.0;
	double _prob_943aa8c3_767e_44a6_9fa7_69de86eef832= 0.0;

	public arithmeticEXTParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class Main_dummy_rule_hope_for_no_collisionsContext extends ParserRuleContext {
		public List<StartContext> start() {
			return getRuleContexts(StartContext.class);
		}
		public StartContext start(int i) {
			return getRuleContext(StartContext.class,i);
		}
		public Main_dummy_rule_hope_for_no_collisionsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_main_dummy_rule_hope_for_no_collisions; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterMain_dummy_rule_hope_for_no_collisions(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitMain_dummy_rule_hope_for_no_collisions(this);
		}
	}

	public final Main_dummy_rule_hope_for_no_collisionsContext main_dummy_rule_hope_for_no_collisions() throws RecognitionException {
		Main_dummy_rule_hope_for_no_collisionsContext _localctx = new Main_dummy_rule_hope_for_no_collisionsContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_main_dummy_rule_hope_for_no_collisions);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(17); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(16);
				start();
				}
				}
				setState(19); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__0) | (1L << T__1) | (1L << T__4) | (1L << T__6) | (1L << T__7) | (1L << T__8) | (1L << T__9) | (1L << T__10) | (1L << T__11) | (1L << T__12) | (1L << T__13) | (1L << T__14) | (1L << T__15) | (1L << T__16) | (1L << T__21) | (1L << T__23))) != 0) );

			_prob_25a67066_8c4d_4a6b_9eb7_57b187a6ef3b = (_25a67066_8c4d_4a6b_9eb7_57b187a6ef3b) != 0 ? _25a67066_8c4d_4a6b_9eb7_57b187a6ef3b/(_25a67066_8c4d_4a6b_9eb7_57b187a6ef3b) : 1.0/1;
			_prob_84c9ec57_f716_4df2_9720_454d02974ba8 = (_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) != 0 ? _84c9ec57_f716_4df2_9720_454d02974ba8/(_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) : 1.0/3;
			_prob_ed4c3af8_ba43_4abc_93a3_263acf446903 = (_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) != 0 ? _ed4c3af8_ba43_4abc_93a3_263acf446903/(_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) : 1.0/3;
			_prob_16f8c1e5_f3e7_412e_8297_320510778a62 = (_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) != 0 ? _16f8c1e5_f3e7_412e_8297_320510778a62/(_ed4c3af8_ba43_4abc_93a3_263acf446903 + _84c9ec57_f716_4df2_9720_454d02974ba8 + _16f8c1e5_f3e7_412e_8297_320510778a62) : 1.0/3;
			_prob_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c = (_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) != 0 ? _0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c/(_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) : 1.0/3;
			_prob_bfc12918_db0c_40bc_84df_98481fcb11ec = (_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) != 0 ? _bfc12918_db0c_40bc_84df_98481fcb11ec/(_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) : 1.0/3;
			_prob_cc82d6ad_25ed_460f_a9c9_d64bdc47586d = (_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) != 0 ? _cc82d6ad_25ed_460f_a9c9_d64bdc47586d/(_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + _bfc12918_db0c_40bc_84df_98481fcb11ec + _cc82d6ad_25ed_460f_a9c9_d64bdc47586d) : 1.0/3;
			_prob_e91a1ede_82b9_4180_ada2_d5608aef67b5 = (_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) != 0 ? _e91a1ede_82b9_4180_ada2_d5608aef67b5/(_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) : 1.0/4;
			_prob_cdd6587e_5c46_4048_bab1_3b75bb0daa4c = (_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) != 0 ? _cdd6587e_5c46_4048_bab1_3b75bb0daa4c/(_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) : 1.0/4;
			_prob_6e6682fc_4517_4b8b_ad5f_64461ba3ed7b = (_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) != 0 ? _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b/(_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) : 1.0/4;
			_prob_58389b8d_df39_4f1b_b749_e6927ae792e4 = (_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) != 0 ? _58389b8d_df39_4f1b_b749_e6927ae792e4/(_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + _58389b8d_df39_4f1b_b749_e6927ae792e4 + _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + _e91a1ede_82b9_4180_ada2_d5608aef67b5) : 1.0/4;
			_prob_5d175fcf_7a7b_428f_96ad_205aba37c7e5 = (_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) != 0 ? _5d175fcf_7a7b_428f_96ad_205aba37c7e5/(_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) : 1.0/3;
			_prob_c07ca19a_b839_4480_83cc_35933bf57c6d = (_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) != 0 ? _c07ca19a_b839_4480_83cc_35933bf57c6d/(_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) : 1.0/3;
			_prob_8e079b6b_87a2_429b_b4be_820e1fc39507 = (_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) != 0 ? _8e079b6b_87a2_429b_b4be_820e1fc39507/(_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + _8e079b6b_87a2_429b_b4be_820e1fc39507 + _c07ca19a_b839_4480_83cc_35933bf57c6d) : 1.0/3;
			_prob_0e615a7b_f485_436f_9864_b3705e7b6a35 = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _0e615a7b_f485_436f_9864_b3705e7b6a35/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_3007af0c_d472_4b02_8dfe_6458ee4dd16b = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _3007af0c_d472_4b02_8dfe_6458ee4dd16b/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_3865f17e_d1ac_460c_b791_5e321bf40b8e = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _3865f17e_d1ac_460c_b791_5e321bf40b8e/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_cf60f941_8297_47e7_93d3_14a5d2cfb58a = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _cf60f941_8297_47e7_93d3_14a5d2cfb58a/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_0debc092_3675_41e0_8b4a_425efd383094 = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _0debc092_3675_41e0_8b4a_425efd383094/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_15408aa6_088b_4b48_a7f0_04e8898cee35 = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _15408aa6_088b_4b48_a7f0_04e8898cee35/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_aca820eb_5a72_4941_b593_63d459e0180d = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _aca820eb_5a72_4941_b593_63d459e0180d/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_1a682da2_5101_4388_8e2e_00900a51ff49 = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _1a682da2_5101_4388_8e2e_00900a51ff49/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_acc6bd49_041c_4dce_9a3d_eefa92b34e6d = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _acc6bd49_041c_4dce_9a3d_eefa92b34e6d/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_70bdf0f7_701f_46e2_a157_ba55bfad7772 = (_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) != 0 ? _70bdf0f7_701f_46e2_a157_ba55bfad7772/(_15408aa6_088b_4b48_a7f0_04e8898cee35 + _aca820eb_5a72_4941_b593_63d459e0180d + _cf60f941_8297_47e7_93d3_14a5d2cfb58a + _acc6bd49_041c_4dce_9a3d_eefa92b34e6d + _0debc092_3675_41e0_8b4a_425efd383094 + _0e615a7b_f485_436f_9864_b3705e7b6a35 + _1a682da2_5101_4388_8e2e_00900a51ff49 + _3865f17e_d1ac_460c_b791_5e321bf40b8e + _3007af0c_d472_4b02_8dfe_6458ee4dd16b + _70bdf0f7_701f_46e2_a157_ba55bfad7772) : 1.0/10;
			_prob_0b697d8c_00a4_4262_acb2_021ebe124eae = (_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) != 0 ? _0b697d8c_00a4_4262_acb2_021ebe124eae/(_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) : 1.0/3;
			_prob_943aa8c3_767e_44a6_9fa7_69de86eef832 = (_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) != 0 ? _943aa8c3_767e_44a6_9fa7_69de86eef832/(_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) : 1.0/3;
			_prob_9e12b4ff_e74d_4097_9cb0_23746944f381 = (_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) != 0 ? _9e12b4ff_e74d_4097_9cb0_23746944f381/(_9e12b4ff_e74d_4097_9cb0_23746944f381 + _943aa8c3_767e_44a6_9fa7_69de86eef832 + _0b697d8c_00a4_4262_acb2_021ebe124eae) : 1.0/3;

			System.out.println(
			"start = " + "exp @@ " + _prob_25a67066_8c4d_4a6b_9eb7_57b187a6ef3b + ";\n" + "exp = " + "term @@ " + _prob_84c9ec57_f716_4df2_9720_454d02974ba8 + " | " + "exp \"-\" term @@ " + _prob_ed4c3af8_ba43_4abc_93a3_263acf446903 + " | " + "exp \"+\" term @@ " + _prob_16f8c1e5_f3e7_412e_8297_320510778a62 + ";\n" + "term = " + "term \"/\" factor @@ " + _prob_0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c + " | " + "term \"*\" factor @@ " + _prob_bfc12918_db0c_40bc_84df_98481fcb11ec + " | " + "factor @@ " + _prob_cc82d6ad_25ed_460f_a9c9_d64bdc47586d + ";\n" + "factor = " + "\"+\" factor @@ " + _prob_e91a1ede_82b9_4180_ada2_d5608aef67b5 + " | " + "\"(\" exp \")\" @@ " + _prob_cdd6587e_5c46_4048_bab1_3b75bb0daa4c + " | " + "digitrec @@ " + _prob_6e6682fc_4517_4b8b_ad5f_64461ba3ed7b + " | " + "\"-\" factor @@ " + _prob_58389b8d_df39_4f1b_b749_e6927ae792e4 + ";\n" + "digitrec = " + "bool @@ " + _prob_5d175fcf_7a7b_428f_96ad_205aba37c7e5 + " | " + "digit @@ " + _prob_c07ca19a_b839_4480_83cc_35933bf57c6d + " | " + "digit digitrec @@ " + _prob_8e079b6b_87a2_429b_b4be_820e1fc39507 + ";\n" + "digit = " + "\"4\" @@ " + _prob_0e615a7b_f485_436f_9864_b3705e7b6a35 + " | " + "\"5\" @@ " + _prob_3007af0c_d472_4b02_8dfe_6458ee4dd16b + " | " + "\"0\" @@ " + _prob_3865f17e_d1ac_460c_b791_5e321bf40b8e + " | " + "\"1\" @@ " + _prob_cf60f941_8297_47e7_93d3_14a5d2cfb58a + " | " + "\"3\" @@ " + _prob_0debc092_3675_41e0_8b4a_425efd383094 + " | " + "\"8\" @@ " + _prob_15408aa6_088b_4b48_a7f0_04e8898cee35 + " | " + "\"7\" @@ " + _prob_aca820eb_5a72_4941_b593_63d459e0180d + " | " + "\"9\" @@ " + _prob_1a682da2_5101_4388_8e2e_00900a51ff49 + " | " + "\"6\" @@ " + _prob_acc6bd49_041c_4dce_9a3d_eefa92b34e6d + " | " + "\"2\" @@ " + _prob_70bdf0f7_701f_46e2_a157_ba55bfad7772 + ";\n" + "bool = " + "\"f\" \"a\" \"l\" \"s\" \"e\" @@ " + _prob_0b697d8c_00a4_4262_acb2_021ebe124eae + " | " + "\"n\" \"u\" \"l\" \"l\" @@ " + _prob_943aa8c3_767e_44a6_9fa7_69de86eef832 + " | " + "\"true\" @@ " + _prob_9e12b4ff_e74d_4097_9cb0_23746944f381 + ";\n");

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class StartContext extends ParserRuleContext {
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterStart(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitStart(this);
		}
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(23);
			exp(0);
			 _25a67066_8c4d_4a6b_9eb7_57b187a6ef3b++; 
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExpContext extends ParserRuleContext {
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public ExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitExp(this);
		}
	}

	public final ExpContext exp() throws RecognitionException {
		return exp(0);
	}

	private ExpContext exp(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpContext _localctx = new ExpContext(_ctx, _parentState);
		ExpContext _prevctx = _localctx;
		int _startState = 4;
		enterRecursionRule(_localctx, 4, RULE_exp, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			setState(27);
			term(0);
			 _84c9ec57_f716_4df2_9720_454d02974ba8++; 
			}
			_ctx.stop = _input.LT(-1);
			setState(42);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(40);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
					case 1:
						{
						_localctx = new ExpContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_exp);
						setState(30);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(31);
						match(T__0);
						setState(32);
						term(0);
						 _ed4c3af8_ba43_4abc_93a3_263acf446903++; 
						}
						break;
					case 2:
						{
						_localctx = new ExpContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_exp);
						setState(35);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(36);
						match(T__1);
						setState(37);
						term(0);
						 _16f8c1e5_f3e7_412e_8297_320510778a62++; 
						}
						break;
					}
					} 
				}
				setState(44);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class TermContext extends ParserRuleContext {
		public FactorContext factor() {
			return getRuleContext(FactorContext.class,0);
		}
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public TermContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_term; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterTerm(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitTerm(this);
		}
	}

	public final TermContext term() throws RecognitionException {
		return term(0);
	}

	private TermContext term(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		TermContext _localctx = new TermContext(_ctx, _parentState);
		TermContext _prevctx = _localctx;
		int _startState = 6;
		enterRecursionRule(_localctx, 6, RULE_term, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			setState(46);
			factor();
			 _cc82d6ad_25ed_460f_a9c9_d64bdc47586d++; 
			}
			_ctx.stop = _input.LT(-1);
			setState(61);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(59);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
					case 1:
						{
						_localctx = new TermContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_term);
						setState(49);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(50);
						match(T__2);
						setState(51);
						factor();
						 _0dc2d63a_0ccf_40ca_9807_c4e7ff9b830c++; 
						}
						break;
					case 2:
						{
						_localctx = new TermContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_term);
						setState(54);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(55);
						match(T__3);
						setState(56);
						factor();
						 _bfc12918_db0c_40bc_84df_98481fcb11ec++; 
						}
						break;
					}
					} 
				}
				setState(63);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class FactorContext extends ParserRuleContext {
		public FactorContext factor() {
			return getRuleContext(FactorContext.class,0);
		}
		public ExpContext exp() {
			return getRuleContext(ExpContext.class,0);
		}
		public DigitrecContext digitrec() {
			return getRuleContext(DigitrecContext.class,0);
		}
		public FactorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_factor; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterFactor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitFactor(this);
		}
	}

	public final FactorContext factor() throws RecognitionException {
		FactorContext _localctx = new FactorContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_factor);
		try {
			setState(80);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				enterOuterAlt(_localctx, 1);
				{
				setState(64);
				match(T__1);
				setState(65);
				factor();
				 _e91a1ede_82b9_4180_ada2_d5608aef67b5++; 
				}
				break;
			case T__4:
				enterOuterAlt(_localctx, 2);
				{
				setState(68);
				match(T__4);
				setState(69);
				exp(0);
				setState(70);
				match(T__5);
				 _cdd6587e_5c46_4048_bab1_3b75bb0daa4c++; 
				}
				break;
			case T__6:
			case T__7:
			case T__8:
			case T__9:
			case T__10:
			case T__11:
			case T__12:
			case T__13:
			case T__14:
			case T__15:
			case T__16:
			case T__21:
			case T__23:
				enterOuterAlt(_localctx, 3);
				{
				setState(73);
				digitrec();
				 _6e6682fc_4517_4b8b_ad5f_64461ba3ed7b++; 
				}
				break;
			case T__0:
				enterOuterAlt(_localctx, 4);
				{
				setState(76);
				match(T__0);
				setState(77);
				factor();
				 _58389b8d_df39_4f1b_b749_e6927ae792e4++; 
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DigitrecContext extends ParserRuleContext {
		public BoolContext bool() {
			return getRuleContext(BoolContext.class,0);
		}
		public DigitContext digit() {
			return getRuleContext(DigitContext.class,0);
		}
		public DigitrecContext digitrec() {
			return getRuleContext(DigitrecContext.class,0);
		}
		public DigitrecContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_digitrec; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterDigitrec(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitDigitrec(this);
		}
	}

	public final DigitrecContext digitrec() throws RecognitionException {
		DigitrecContext _localctx = new DigitrecContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_digitrec);
		try {
			setState(92);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(82);
				bool();
				 _5d175fcf_7a7b_428f_96ad_205aba37c7e5++; 
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(85);
				digit();
				 _c07ca19a_b839_4480_83cc_35933bf57c6d++; 
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(88);
				digit();
				setState(89);
				digitrec();
				 _8e079b6b_87a2_429b_b4be_820e1fc39507++; 
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DigitContext extends ParserRuleContext {
		public DigitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_digit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterDigit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitDigit(this);
		}
	}

	public final DigitContext digit() throws RecognitionException {
		DigitContext _localctx = new DigitContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_digit);
		try {
			setState(114);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__6:
				enterOuterAlt(_localctx, 1);
				{
				setState(94);
				match(T__6);
				 _0e615a7b_f485_436f_9864_b3705e7b6a35++; 
				}
				break;
			case T__7:
				enterOuterAlt(_localctx, 2);
				{
				setState(96);
				match(T__7);
				 _3007af0c_d472_4b02_8dfe_6458ee4dd16b++; 
				}
				break;
			case T__8:
				enterOuterAlt(_localctx, 3);
				{
				setState(98);
				match(T__8);
				 _3865f17e_d1ac_460c_b791_5e321bf40b8e++; 
				}
				break;
			case T__9:
				enterOuterAlt(_localctx, 4);
				{
				setState(100);
				match(T__9);
				 _cf60f941_8297_47e7_93d3_14a5d2cfb58a++; 
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 5);
				{
				setState(102);
				match(T__10);
				 _0debc092_3675_41e0_8b4a_425efd383094++; 
				}
				break;
			case T__11:
				enterOuterAlt(_localctx, 6);
				{
				setState(104);
				match(T__11);
				 _15408aa6_088b_4b48_a7f0_04e8898cee35++; 
				}
				break;
			case T__12:
				enterOuterAlt(_localctx, 7);
				{
				setState(106);
				match(T__12);
				 _aca820eb_5a72_4941_b593_63d459e0180d++; 
				}
				break;
			case T__13:
				enterOuterAlt(_localctx, 8);
				{
				setState(108);
				match(T__13);
				 _1a682da2_5101_4388_8e2e_00900a51ff49++; 
				}
				break;
			case T__14:
				enterOuterAlt(_localctx, 9);
				{
				setState(110);
				match(T__14);
				 _acc6bd49_041c_4dce_9a3d_eefa92b34e6d++; 
				}
				break;
			case T__15:
				enterOuterAlt(_localctx, 10);
				{
				setState(112);
				match(T__15);
				 _70bdf0f7_701f_46e2_a157_ba55bfad7772++; 
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BoolContext extends ParserRuleContext {
		public BoolContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).enterBool(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof arithmeticEXTListener ) ((arithmeticEXTListener)listener).exitBool(this);
		}
	}

	public final BoolContext bool() throws RecognitionException {
		BoolContext _localctx = new BoolContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_bool);
		try {
			setState(129);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__16:
				enterOuterAlt(_localctx, 1);
				{
				setState(116);
				match(T__16);
				setState(117);
				match(T__17);
				setState(118);
				match(T__18);
				setState(119);
				match(T__19);
				setState(120);
				match(T__20);
				 _0b697d8c_00a4_4262_acb2_021ebe124eae++; 
				}
				break;
			case T__21:
				enterOuterAlt(_localctx, 2);
				{
				setState(122);
				match(T__21);
				setState(123);
				match(T__22);
				setState(124);
				match(T__18);
				setState(125);
				match(T__18);
				 _943aa8c3_767e_44a6_9fa7_69de86eef832++; 
				}
				break;
			case T__23:
				enterOuterAlt(_localctx, 3);
				{
				setState(127);
				match(T__23);
				 _9e12b4ff_e74d_4097_9cb0_23746944f381++; 
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 2:
			return exp_sempred((ExpContext)_localctx, predIndex);
		case 3:
			return term_sempred((TermContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean exp_sempred(ExpContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 2);
		case 1:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean term_sempred(TermContext _localctx, int predIndex) {
		switch (predIndex) {
		case 2:
			return precpred(_ctx, 3);
		case 3:
			return precpred(_ctx, 2);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33\u0086\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\3\2\6\2\24\n"+
		"\2\r\2\16\2\25\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4"+
		"\3\4\3\4\3\4\3\4\3\4\7\4+\n\4\f\4\16\4.\13\4\3\5\3\5\3\5\3\5\3\5\3\5\3"+
		"\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\7\5>\n\5\f\5\16\5A\13\5\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6S\n\6\3\7\3\7\3\7"+
		"\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7_\n\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b"+
		"\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\bu\n\b\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u0084\n\t\3\t\2\4\6\b\n\2"+
		"\4\6\b\n\f\16\20\2\2\2\u0092\2\23\3\2\2\2\4\31\3\2\2\2\6\34\3\2\2\2\b"+
		"/\3\2\2\2\nR\3\2\2\2\f^\3\2\2\2\16t\3\2\2\2\20\u0083\3\2\2\2\22\24\5\4"+
		"\3\2\23\22\3\2\2\2\24\25\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2\26\27\3\2"+
		"\2\2\27\30\b\2\1\2\30\3\3\2\2\2\31\32\5\6\4\2\32\33\b\3\1\2\33\5\3\2\2"+
		"\2\34\35\b\4\1\2\35\36\5\b\5\2\36\37\b\4\1\2\37,\3\2\2\2 !\f\4\2\2!\""+
		"\7\3\2\2\"#\5\b\5\2#$\b\4\1\2$+\3\2\2\2%&\f\3\2\2&\'\7\4\2\2\'(\5\b\5"+
		"\2()\b\4\1\2)+\3\2\2\2* \3\2\2\2*%\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2"+
		"\2-\7\3\2\2\2.,\3\2\2\2/\60\b\5\1\2\60\61\5\n\6\2\61\62\b\5\1\2\62?\3"+
		"\2\2\2\63\64\f\5\2\2\64\65\7\5\2\2\65\66\5\n\6\2\66\67\b\5\1\2\67>\3\2"+
		"\2\289\f\4\2\29:\7\6\2\2:;\5\n\6\2;<\b\5\1\2<>\3\2\2\2=\63\3\2\2\2=8\3"+
		"\2\2\2>A\3\2\2\2?=\3\2\2\2?@\3\2\2\2@\t\3\2\2\2A?\3\2\2\2BC\7\4\2\2CD"+
		"\5\n\6\2DE\b\6\1\2ES\3\2\2\2FG\7\7\2\2GH\5\6\4\2HI\7\b\2\2IJ\b\6\1\2J"+
		"S\3\2\2\2KL\5\f\7\2LM\b\6\1\2MS\3\2\2\2NO\7\3\2\2OP\5\n\6\2PQ\b\6\1\2"+
		"QS\3\2\2\2RB\3\2\2\2RF\3\2\2\2RK\3\2\2\2RN\3\2\2\2S\13\3\2\2\2TU\5\20"+
		"\t\2UV\b\7\1\2V_\3\2\2\2WX\5\16\b\2XY\b\7\1\2Y_\3\2\2\2Z[\5\16\b\2[\\"+
		"\5\f\7\2\\]\b\7\1\2]_\3\2\2\2^T\3\2\2\2^W\3\2\2\2^Z\3\2\2\2_\r\3\2\2\2"+
		"`a\7\t\2\2au\b\b\1\2bc\7\n\2\2cu\b\b\1\2de\7\13\2\2eu\b\b\1\2fg\7\f\2"+
		"\2gu\b\b\1\2hi\7\r\2\2iu\b\b\1\2jk\7\16\2\2ku\b\b\1\2lm\7\17\2\2mu\b\b"+
		"\1\2no\7\20\2\2ou\b\b\1\2pq\7\21\2\2qu\b\b\1\2rs\7\22\2\2su\b\b\1\2t`"+
		"\3\2\2\2tb\3\2\2\2td\3\2\2\2tf\3\2\2\2th\3\2\2\2tj\3\2\2\2tl\3\2\2\2t"+
		"n\3\2\2\2tp\3\2\2\2tr\3\2\2\2u\17\3\2\2\2vw\7\23\2\2wx\7\24\2\2xy\7\25"+
		"\2\2yz\7\26\2\2z{\7\27\2\2{\u0084\b\t\1\2|}\7\30\2\2}~\7\31\2\2~\177\7"+
		"\25\2\2\177\u0080\7\25\2\2\u0080\u0084\b\t\1\2\u0081\u0082\7\32\2\2\u0082"+
		"\u0084\b\t\1\2\u0083v\3\2\2\2\u0083|\3\2\2\2\u0083\u0081\3\2\2\2\u0084"+
		"\21\3\2\2\2\13\25*,=?R^t\u0083";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}