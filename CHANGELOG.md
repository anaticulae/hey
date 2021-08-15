# changelog

Every noteable change is logged here.

## v5.11.9

### Feature

* skip too few text style extractor (93750e7068f5)

### Fix

* skip empty selection (050dcfa935bd)

## v5.11.8

### Feature

* use images folder after moving figures (3b64330d8d1e)

## v5.11.7

## v5.11.6

### Feature

* replace linero with tablero (8ea98a306755)

## v5.11.5

## v5.11.4

## v5.11.3

## v5.11.2

## v5.11.1

### Fix

* do not run vector for too few data (6fdf645d9539)

## v5.11.0

### Feature

* extend interface to configure valid headline checker (2bb5c534195b)
* skip headline cluster with too many white spaces (0b1fc28accf4)

### Fix

* adjust valid range (b96e68a62aec)

### Documentation

* fix spelling error (9e0b4ffc82f1)

## v5.10.1

### Fix

* add missing import (c6587201f1a1)

## v5.10.0

### Feature

* add method to extract headlines from data (f7398d6ad44a)
* add method to create vector data from python (c738775d050f)

## v5.9.0

### Feature

* remove non chapter headlines out of first headline group (c103fce3042a)
* use upper cased rate to improve headline clustering (0a914be32f06)
* add public headline extractor interface (fbb03202afc9)
* group headlines by level (bf48e79e7908)
* add method to extract headlines (693d72308240)
* use more precise text size (bc4f02384ea9)
* shrink valid area of headlines (08b3855be182)
* skip magic data in headline processing (126e1b61a31f)
* split magic step into two separate steps (58e309e44cc3)

### Fix

* only skip current item if already used (194741b5e8e3)
* fix spelling error (07690c6b1809)
* handle fewer than four headlines correctly (8d42db0e3989)
* handle single line page (c5dc6bb4732e)

## v5.8.0

### Feature

* skip Kapitel-1 as headline pattern (677cb6fe4094)
* increase maximum xdiff of headline (e6abdca5ad36)
* detect distance before and after headlines (3adb7d74047a)
* add before and after to cluster data (e95019366bcc)
* add method to rotate arrays (1e8e74b0ceb9)
* protect interface against misusing (60f35dd8a16b)
* add simplified run interface (953670693c18)
* add font family detector (1f8af07bc637)
* disable warnings (649802a24443)
* add headline style selector (f6807f3762a5)
* use numpy seed for having reproduce able results (04687beb9f88)
* do not detect selective bold as common bold line (a4a661793ad1)
* add cluster decider (7db648e8b596)
* parse document into feature vector (6f8d944516b6)
* use kmean to cluster group of styles (e14fe58a0c1c)
* add method to connect list of pages (0d218ae597c9)

### Fix

* do not convert single value (4286466530b3)
* do not skip headlines with small left border (f368d5d1580e)
* most of elements must be bold to be bold (b9d6256b04c9)
* skip empty pages (e77ed864fd01)
* use non zeros values for disabled feature (b2685c1f0343)

## v5.7.0

### Feature

* determine magic for normal content (fc35aa903fb6)
* skip --table step if linero_table resource is not available (6c8c5e70b124)

## v5.6.5

### Feature

* externalize parameter to increase configurability (59d7795a18d5)

## v5.6.4

### Documentation

* Happy New Year! (8bbb649be404)

## v5.6.3

### Feature

* use elements to improve headline extractor (02645bd0df4d)

## v5.6.2

### Fix

* fix accessing error, return empty data instead (e52339239ec0)

## v5.6.1

### Feature

* add option to disable line intent clustering (f617ad4326be)

### Documentation

* clarify interface (93babc1bf764)

## v5.6.0

### Feature

* use left bounding to improve headline cluster (af1072470e17)
* add left validation option (eb5877f974a8)

## v5.5.4

## v5.5.3

## v5.5.2

### Feature

* add multi process flag (c5a32fb894e1)

## v5.5.1

## v5.5.0

### Feature

* extend image detection key word list (62e2c13a02b6)
* add multiple line formula detection (3ce8e02abf61)

## v5.4.0

### Feature

* use more likely item first (e3d7232aebfd)

## v5.3.0

### Feature

* add multiple-page-list resolver (ceda1dc6b340)
* improve headline style detector (908abd1debf6)
* use magic data to improve headline style detector (4d27a8ecc375)

### Fix

* improve headline style detector (efa5f5b1f6c1)
* adjust order of magic detection (5f03bcc98bfa)

## v5.2.0

### Feature

* enable collecting caption before item (23d69faf29c0)
* unify extracted captions (227779b18a07)

### Documentation

* add information about tables which are stored as image (b04a1737f252)

## v5.1.1

### Fix

* do not access not detected style (a4d3fc61614b)

## v5.1.0

### Feature

* detect captions of tables which are printed as image (a94519034956)
* support English captions (e30c59eae9df)
* adjust holy value of justified text (7a2107442d9b)
* introduce JUSTIFIED constant to increase code readability (336216c71856)
* add support for multiple line captions in magic (d85b5a6ab113)

### Fix

* determine most common font correctly (ef7cb8d0acd9)

## v5.0.0

### Feature

* add filter to reduce false detected headline style (7acc278712ca)
* add page flag to parser (91533f80b835)
* add page attribute to TextProperty (6cb982e23479)
* remove column/alternate layout extractor (28851187b94b)
* add logging information of doctextstyle run (224073ff8945)
* use complex font selector to cluster possible headlines (db8abc100650)
* do not judge to short content as headline (f878d86f15da)
* disable headline determining strategy (83fe01efa283)
* extend collect caption by equal following text (61b30771fd7a)

### Fix

* do not extract style for very few pages (7c2a23aeb07f)

## v4.0.1

## v4.0.0

### Feature

* remove moved groupme code (a896d516df77)

### Documentation

* remove moved groupme documentation (62f1751231b8)

## v3.11.1

### Fix

* set plain number strategy as a backup strategy only (0514dc27107b)

## v3.11.0

### Feature

* extend negative headline list (0cd3e943c2b8)
* disable strategy if result seem not to be correct (3f25daa2cd74)
* add plain number footnotes parser (fa789d80f186)
* introduce tolerance to increase matching (57d472c921d6)

### Fix

* adjust toc parser for figure table parsing (c9a468b3e563)
* run caption before magic (b8c285c31f66)
* fix numbered level (0dce9fe062d7)

## v3.10.0

### Feature

* improve detection quality (e1aa9111d180)
* improve common header extraction strategy (3a7e762adc66)
* add default path to pagesize loader (3c3f3f683559)
* log missing optional resources (f247a8cbc5b5)

### Fix

* determine page number for non zero index data correctly (a61abc7b7b81)
* strip newlines for both header elements (36d08a251bd3)
* adjust holy value to parse bachelor241 correctly (073a15601159)

### Documentation

* extend interface documentation (1306120652bb)

## v3.9.0

### Feature

* add blockquote style extractor (8b5842b32cc7)
* extract left/right text positions (ec28bfbd2129)
* improve headline detection on content only pages (125744a17086)

### Fix

* increase required debugging level (52237d0fb48b)
* decrease minimal distance between page number and footer horizontal (8838304aeec9)

## v3.8.1

### Fix

* add tolerance to improve headline cluster (e8c4f25d6a7a)

## v3.8.0

### Feature

* move extractor rawmaker config to separate config (ce9c289199b7)
* add textflow flag to example generator (624e56411ed1)

## v3.7.2

### Fix

* do not fail if line gap computation is not possible (5359b39d45b7)
* add missing cluster category (a8b9ffe82269)
* disable strategy if data is not suitable (1f59d781e8a7)

## v3.7.1

### Feature

* add full concept for `todolist` also (2cf624390f6d)

## v3.7.0

### Feature

* add full flag to enable every extraction step (7f0783600530)
* disable every generator step as default (f292a685bf31)

## v3.6.1

## v3.6.0

### Feature

* add extracted figures to magic computation (959ca5c75f9d)
* add table result to magic analyzer (eca9455fdc35)
* add column figure extractor approach (b62be67f8416)
* use normal text extraction data (a9a2827895b0)

### Fix

* move level check later to avoid conversion problems (929ba61b8339)
* skip miss detected enumeration in tables (4435b4703793)
* increase required logging level (92196cc2f17e)
* fix percent definition (43ef1b718833)
* adjust logging message (1e593f828290)
* add workaround to compute text style statistics (ce8d87399eef)

## v3.5.3

## v3.5.2

## v3.5.1

## v3.5.0

### Feature

* add figure caption extractor (e09c552df3a3)
* add table caption extractor (9479c1fe9bf7)
* extend image caption detector magic name (da53850cfa38)
* add caption option to example data generator (ece22175cae5)
* add captions analysis (67a11bc213bd)
* add merging step to merge different captions (94d8d3da81ea)
* add image caption extractor (076144413cfa)
* add caption cli (d0d5434a1ca2)

### Fix

* handle non zero indexes distances correctly (1eaefbd8d6a7)

### Documentation

* remove outdated readme information (265f99c71f75)

## v3.4.0

### Feature

* add formula decider step (5630d375e976)

## v3.3.0

### Feature

* add blockquote detector (603f009595c1)

## v3.2.0

### Feature

* add magic selector to generate test data (439f432b11f6)
* add magic content path resolving method (893349bbb5d1)

## v3.1.0

### Feature

* add optional blockquotes checker step (b00503663012)
* add list detector (76edfb1dd9eb)
* add method to dump and load magic data (a562217fab9f)
* add basic cli interface and testing (46b4c3ff4926)

### Fix

* disable broken data generator (91bf532831d5)

## v3.0.1

## v3.0.0

## v2.9.0

### Feature

* add slash pattern to author parser (25da0afb716c)
* use `tech` parser to analyse column bib ref layout (de86623d600e)
* add pages parser to `freeand` parser (2c970a2cc832)
* add multiple author parser (ad1a2e3e65fe)
* add multiple authors pattern parser (8291b18cbf45)
* add freeand pattern parser (68baf18aa1b4)
* add tech long pattern parser (9e79017cf5fd)
* use improved technical parser (9ca1bdab5800)
* add technical reference parser (7224f3e859c1)

## v2.8.0

### Feature

* add tabletable extractor (07b9a8b00206)
* add figurestep to extract table of figures (f9c3b505b824)
* limit toc localisation to first 15 pages (f86b550399ae)
* limit page length of toc parser (345e7f926ffb)
* reduce min length to double instead of triple lines (e0c0fc7f545f)

### Fix

* use more complex and correct level determiner (a5ed97e6f2bf)
* skip empty pages (8be341e0acf6)
* fix debug message (cde634b2a841)

## v2.7.6

### Feature

* extend title type extractor (e4062946eceb)

### Fix

* round to have better groups (9d984e24ca1c)
* round extracted left/right text distance result (ec40a44d8560)

## v2.7.5

### Fix

* avoid error on very short documents (83e583b17192)

## v2.7.4

### Feature

* add method to detect justification of text (20aea61c6ab4)
* extract left and right text bounds (569e320ee4bf)
* add step to extract text bounding of content (afb46770b056)

## v2.7.3

## v2.7.2

### Feature

* limit regex to reduce mismatching (b7f15bffb3f7)

### Fix

* skip empty footnotes and signal error (2ab2d69b7150)
* ensure to use correct data/datatype (f208e3194835)
* fix accessing correct data type (33219b755447)

## v2.7.1

### Fix

* do not fail on empty content border (2569bbd1e232)

## v2.7.0

### Feature

* add different border extractor for different page sizes (363ec6d71188)
* extract content mostly used page content border (91dede7d93a9)
* add method to load border leftright (0cea513e3e4f)
* write extracted page size to docstyle result (6b2e00e4a4e1)
* determine major and other paper sizes (14d492dcf055)
* add page and content dimension (8ae84fd320d5)
* add module to determines paths of written content (28b69ed89de5)
* round text distances to requested accuracy (b1b5f788a99d)

### Fix

* use more safe approach (b97c76a80dab)

## v2.6.1

## v2.6.0

### Feature

* add method to extract biggest valid cluster (f890ef6a7e70)
* ignore to short titles on possible title page (4670bad75193)
* extend university list (5bb1458891e2)

### Fix

* shrink toc extraction to document start (4b5a2a8c8d14)
* change test and add hints (9e9d09ebd276)
* add invalid parsed items to judge parsing quality (08d468e57dc1)
* group toc groups correctly (05ae1d6b4764)
* add missing `raw_location` (f94a950c2216)
* disable outlines cause extraction requires to much time (6a69e8ab675a)

## v2.5.0

### Feature

* add profile option to investigate parser time problems (1d722a10a44a)

### Fix

* enable old test (87b8999ae87e)
* improve performance (73c3ca8cf862)
* improve title parser speed (47564bcaab99)

## v2.4.3

### Feature

* add doctextstyle to test data generator (188fe3866e09)

### Fix

* add missing import (101f420bede2)

## v2.4.2

## v2.4.1

## v2.4.0

### Feature

* add description of the tool purpose (9c6cac6e0609)
* add command line interface (361c269a2d31)
* extract common doc textstyle (201731cedb06)
* add collection to store expected docstyle (7470aa5f1097)
* add paragraph distance gap extractor (494595817111)
* add footer style extraction detector (d3186937c355)
* add parameter to return selected cluster (e24a0f442efd)
* add first and second headline extractor (babddcac6670)
* add method to determine pagenumber style (61cba5899519)
* add distance to element before (9284cfb0cb32)
* add method to determine default text size/font of document (753765161619)
* cluster extracted text attributes (15f370ae5eea)
* add basic textstyle evaluator (ce492ae5e0f6)
* extend letter start parsing (88b83370db15)
* extend allowed accepted character in toc text (c4962b0ea5db)

### Fix

* use most common font style instead of first font size (c48566188c36)
* do not produce None at big failure counts (68387f036a27)
* catch empty line gap (2ca490c35cf2)
* ensure to parse vowels correctly (0b6d52821556)

## v2.3.1

## v2.3.0

### Feature

* extend title detection black list (be725b852b80)
* store parsing location to use as linter location (ca5a639a8958)
* save location where toc was parsed (d72ac11eed35)

### Fix

* fix more linter warnings (6dc1b182de0d)
* fix more linter warnings (da977b98a542)
* fix more linter warnings (fa9b66980254)
* solve some linter warnings (d051191e4036)

### Documentation

* fix interface documentation (ce2437ac9a35)

## v2.2.0

### Feature

* skip empty lines to avoid detecting single words as toc content (7357ff604818)
* use oneline input cause we expect better easier toc parsing (2c123327c3c4)
* extend no level pattern (20b5066c66e7)
* count parsed level to extend toc decider strategy (003459c1e31c)
* improve regex parser due run grouping layout before (5dd06f55b063)
* normalize white spaces cause of bad formatted title page (65a29aaa9eaa)
* extend toc letter parser (59b002f51c9c)
* extended dotted pattern (655b65ab7944)
* extend dotted and number parser (4370211dce7f)
* add optional debugging information (f3e1dc8ba01e)
* extend interface documentation (7562b828b2cf)

### Fix

* extend linter white list (ee3979308646)
* ensure to handle lines with dotted correctly (7a9a72c8cac9)
* solve linter warnings (21841cab7bb9)

## v2.1.0

### Feature

* do not parse thesis type as title (60bcbf096c50)
* support lowercase and uppercase thesis type (e455abd257fb)
* add semester date parser (57b70a7e53a1)
* extend person parser (3a34b77ac26d)
* handle specials chars correctly (1b205a3e2546)
* extend universities (a2f4d412c99d)
* parsing persons with academic title after persons name (e9c6c5452788)
* extend list of know universities (ed1caeb065b8)
* add optional female endings (a01c0b018b0b)
* add method to determine extracted titlepage path (5e255f8b74d8)

### Fix

* detect bachelor76 page0 as valid title page example (b67efffb76fb)
* do not fail without detecting title (f030fd6a0c77)

### Documentation

* extend interface documentation (dc29dec1e403)

## v2.0.17

### Fix

* by pass problem in name parser (8554451dbc68)

### Documentation

* extend interface documentation (f4ce77bc7ce2)

## v2.0.16

## v2.0.15

## v2.0.14

### Feature

* add optional pages pattern to shrink range of extraction (5fe3c987b3ec)

### Fix

* ensure to have valid pageheight (3f230c401cfd)

## v2.0.13

### Feature

* separate run and todo generator step (40b4829063b2)

### Fix

* disable sorting (2cb00ae0115e)

## v2.0.12

## v2.0.11

### Fix

* sort files cause simplify expects sorted files (c295ce036b93)
* fix typo and remove unnecessary option (d448a6f8faf0)

## v2.0.10

## v2.0.9

## v2.0.8

## v2.0.7

### Feature

* add logging step (deabb4968724)

## v2.0.6

### Fix

* use strategy instead of fixed diff (b69095405cc1)
* adjust holy value (fe4a7ed819df)

## v2.0.5

### Feature

* enable selective page selection (3924ee219eee)

### Fix

* use pagenumber to avoid handling empty special cases (3546d1a2dbe8)
* adjust correct pdf page extracted page number (f7a6905b0a01)

## v2.0.4

### Fix

* do not let parser fail (66e7e2a0a58d)
* skip footnote when not able to convert footnote number (073e9d888d8a)

## v2.0.3

### Feature

* improve multiline footnote parser (6ed7db9ff1e0)

### Fix

* ensure that negative detection does not break analysis, log instead (b45e24f65149)
* do not return empty moving footer (7cf04a8502d7)
* make toc line matching harder (0058077dd266)
* adjust holy value to solve failing test (89c0cf31ffe2)
* ensure that default variable is handled correctly (95069aa99ef2)

## v2.0.2

## v2.0.1

## v2.0.0

### Feature

* make example run selective (f21dc889b773)

### Fix

* catch to few items (b5ddba61c1ab)
* ensure to handle partial pages correctly (451dddf183f6)
* add stolen code from words package (e16f073a4b4d)

## v1.19.1

## v1.19.0

### Feature

* introduce min likelihood to disable feature (1c6b77ae59b2)
* no toc after page 30 - very weak (d475aaee5d4c)
* add method to extract sections from path (d6a8c21a2ad2)
* add bib, legal and abbreviation likelihood to decider (d6e489046f5b)
* add bib likelihood extract step - cli (b8ec664b3b4c)
* add likelihood detector for bibliography (717655f4d277)
* use multi formed analysis (c8c0bc800610)
* make bibliography sortable (4679a40a3b9c)

### Fix

* shrink test result cause appendix is recognized correctly now (6ff97be1d794)
* ensure that at least one feature is selected (6825ec082c10)
* extend bib likelihood detector (c51965f10152)
* do not ignore very high rated features (5ef95028d506)
* align tests with new interfaces (91205938f62d)
* fix name (d8c1f9251fc5)
* reduce minimal required trust to have multiple features (7b2b2657bce2)

## v1.18.0

### Feature

* extend pattern to split author/year and other data (52f5a6434d7c)
* unite hurenkind over two pages correctly (1b19b081e553)
* ensure to handle start with title item (8c552e07a812)
* extend alternate approach to parse pages with few bibs (a6c67b9ed80f)
* support global lining points (56fc67bc501e)
* add approach to handle multi page likelihoods (ce944aaeac68)
* extend section toc likelihood pattern (6711d4e999de)
* enable shrink title page detector (734182618ea7)
* add alternate strategy to bibliography parser (e05d720ba13e)
* add bibliography extractor to support [HELM10]-pattern (281fd318e96e)
* add alternate geometry parser (c8dd46119825)
* extend strategy logging and remove unused code (62b6beaf3717)
* add step to extract literature table (baaf6a5747be)
* add path module to determine output path (a6393a4e9f00)
* add double column layout parser (7eb365e01152)

### Fix

* solve multiple font (e68e55ee789e)
* ensure to handle invalid bibs correctly (4da45366c5d7)

## v1.17.4

### Feature

* move leftright border detector from decider (19746141807f)
* add legal step to detect location of Eidesstattliche Erklaerung (8bfb10ace75f)
* improve type defintion (e4a5dac631ea)

## v1.17.3

## v1.17.2

### Feature

* make abbreviation sortable (b3e7c93de81b)
* add method to sort words alphabetically (3a3164644493)
* introduce Cluster to formalize clustering (fd8cbedf6f58)
* use navigators page number to support selective processing (6b423f7f76ff)
* ensure that min elements is less one (e461df72629f)
* add minimal feature count (76ff8bb4e2b0)

### Fix

* avoid selecting empty page height (2681a016ad5c)

## v1.17.1

### Feature

* add abbreviation table parser step to groupme (335e2eb35c59)

### Fix

* skip non column layout (e640fd56470e)

## v1.17.0

### Feature

* add abbreviation step to command line interface (9042a3b522e2)
* add step to determine abbreviation likelihood (9490fd4b1e4d)
* extend blacklist for sentence parser (d535b262c9e4)
* add parser to extract lists of words and statistics from page (9da30366bfa4)
* add parser to convert texts into single words (6d65669334b7)
* add option to disable input validation (5f0a0d989e32)
* do not parse non closed sentences (1c72d9d4edfa)
* add abbreviation step to parse abbreviation out of text (6cd737dc3af3)
* add method to dump and load abbreviations (576dd45c86d1)
* extend DUDEN white list and remove duplication (1a75d2b70a0a)
* add optional position to store parse location (18d387e797ba)
* add method to split sentences into words (4ce5ef54c15d)
* add method to check for a sentence (6227b1fccbf1)
* support multiple lines (50b131af7a6c)
* add path module to access generated path (a193b8398533)
* ensure that algorithm has correct assumptions (744dd074bd13)
* use simple parser only as backup (d2bcf54d74e9)
* remove trailing white spaces of shortcut (29c7e34c3192)
* add judging strategy to abbreviation (c17202e4d26d)
* add abbreviation geometry strategy (725c3099a73b)
* add classifier to group list of number by distance (000de5d97f0d)
* sort cluster by element size descending (a3927aa65e30)
* move simple parser to first simple strategy (ba34d295add3)
* add pattern to implement abbreviation parser strategies (a61aee3a1da2)
* add simple abbreviation extractor (bbb0d56e3e25)

### Fix

* extend word splitter (b04e455cf524)
* fix cluster computation (4c84481154b4)
* increase tolerance to solve master116 example (9662a88eb4a6)
* use y1 baseline to improve grouping quality (ead0b08f8dc4)
* disable broken foot note parser test (71feecfd9221)
* change expected size to new font size rounding (5c8f7feeedd5)

### Documentation

* add introduction to introduce sections feature (9a69f4695488)

## v1.16.1

### Feature

* add distance feature to cli (1b0d5d6541f7)

## v1.16.0

### Feature

* add distance feature (18e935b39307)
* add tolerance to inside detection (05966311a689)
* extend path module (5e9a21dc0895)
* add area step to command line interface (cade977e92ad)
* save area of non textual elements (77c0d29de7df)
* add method to dump and load detected areas (ca3c67de15c0)
* add step area to judge elements on page (0141b2444a9a)
* add method to determine minimal count of required rectangles (6e063f354505)
* add bounding rectangle checker (3690735ae1ba)

### Documentation

* extend interface documentation (46bd0eaee5d6)

## v1.15.9

## v1.15.8

### Fix

* fix generated outpath names (d7e91557c390)

## v1.15.7

### Documentation

* fix title page introduction (459638064943)

## v1.15.6

### Fix

* log that textnavigator was not loaded (c00a96c1b987)

## v1.15.5

## v1.15.4

### Fix

* fix detecting page number (a75051a58bef)

## v1.15.3

### Feature

* extract raw page number and converted value (f4292cfb3e9b)
* add method to find item in navigator by BoundingBox (411607f51c0d)

## v1.15.2

## v1.15.1

### Fix

* add detector run to example data generator (3981793cb43f)

### Documentation

* add purpose of test data generator (4e5650c20864)

## v1.15.0

### Feature

* add missing resources to footer extraction step (25a4ca4b8c7e)
* use highnotes parser and modify holy notes (f521890e7cc4)
* add style to parsed footraw-note (8bd0044c32dc)
* add font information to pagetextnavigator if provided (0df71d53d10d)
* add method to parse footer with footnotes (0671139d4673)
* add method to merge highnotes in horizontal line (01808530d52b)
* add Bounding to extracted Highnote (f131c36d8c46)
* add method to split content by Highnote (0cb2d3b604b0)
* create separate package to add more detection logic (6321f606adf5)
* parse multiline footnotes (0a94785a2234)

### Fix

* fix spelling error (be363d911f4d)
* avoid determine min of empty sequence (229b43fcf9c2)
* resolve cyclic import (27f92d0fa0c7)
* do not modify parsed input data (884a683df2f5)

### Documentation

* extend interface documentation (c329e51de7ce)

## v1.14.12

## v1.14.11

## v1.14.10

### Feature

* extend pattern to parse on multiple lines. (935d092bd671)

### Fix

* extend check that lowest examiner is not detected as author (0147b9846dfc)
* extend prof-detection pattern (f9f3775111be)
* support multiline title (07045324605c)
* fix date parser (996d195216bd)
* fix accessing correct variable (271adc13f57d)

### Documentation

* extend title parser documentation (eacf2b2d71e2)

## v1.14.9

### Fix

* log page validations and do not let application fail (3914fcf2bde3)

## v1.14.8

## v1.14.7

### Feature

* add method to ensure unique pages (e4441d39b3b1)
* do not process item without and header and footer (14686d862514)
* ensure that extract gets sorted pages and produces sorted results (2c1f66572a78)
* ensure that sync gets sorted iterators (a187810d7384)
* extend person parser (f11716ac2816)

### Fix

* create correct pytest test names with forward slashs (bbdd916e41eb)
* sort results by page (79ddbffd1a9b)
* fix test after removing duplicates (b0b886828f28)
* fix pages extract to ensure sorted pages (64d12ce3c693)
* fix strategy selector (98dcf430015e)

## v1.14.6

### Documentation

* Happy New Year! (8bb16846ed5d)

## v1.14.5

## v1.14.4

## v1.14.3

### Feature

* add method to determine toc output path (16e7c42cfca4)

## v1.14.2

### Feature

* reduce example generation time due multi processing (25fb9aee9af6)

### Fix

* return None if no valid TitlePage can be selected (931d19ee3dc6)
* ignore numbered invalid dr. title (1ad4fec582c9)

## v1.14.1

### Feature

* reduce miss detection of title pages (ea5d24c098e5)

## v1.14.0

### Feature

* extend title page parser (ded7aff53250)

### Fix

* parse none existing institution as None (622f20f8113d)

## v1.13.6

### Fix

* fix problem with starting white page (2b2ab90677e6)

## v1.13.5

### Feature

* check if directory exists externally (1951cf5e46a1)

## v1.13.4

### Feature

* add `raw` and `page` to have more data for decider/validator (a7fae9bde03e)

## v1.13.3

### Fix

* report toc extraction problem instead of failing with error (05d37409fbbf)

## v1.13.2

### Fix

* enable to process all pages (e9cd3ee8c0e3)

## v1.13.1

### Feature

* add example data generator for following data unit (4ab8f384305b)

### Documentation

* add missing headline to last release page (8c217b11dd59)

## v1.13.0

### Feature

* add new table of content extraction approach (cbac8eedf3b7)
* add method to create PageTextContentNavigators (8dbd1959a88b)
* support parsing PageTextNavigator (57fba93d27e4)
* add method to split container by key function (96ed405c2a6b)
* add method to load data required by toc extractor (889ad053c49b)
* remove outdated chapter extraction approach (58652631f616)
* add geometric strategy to extract table of content (a81c1669ad04)
* add method to determine text feed of document (0ac997b3a7b4)
* add toc extraction decider strategy (03c21b5b5e8e)
* return empty list if group empty list (12e33cfc20d3)
* extend toc regex parser (fa2ac86e14c6)
* disable checking content border to parse headlines correctly (c41e741c2ad5)
* do not detect normal text as common-text-header (90918c8009a6)
* add new header extraction strategy (887046fbb784)
* use text as __repr__ for TextInfo to ease print debugging (07b02d85b48e)
* extend line parser to parse bachelor111 toc correctly (5166b213c111)
* extend toc-regex-strategy to support more pattern (afda1be76415)
* add basic toc extractor strategy (25d1c065bcf3)
* add AppendixLevel to support more toc lines (68d065abd652)
* add method to group headlines depending on chapter (eae872622d31)
* introduce regex text package to unify regex (8c4d9ba29b92)
* add toc geometry strategy (47feea746c55)
* extend regex headline parser (af0339c2f784)
* add method to parse single headline (b5e8075826fa)
* extend interface documentation (0f4052b246a9)
* add parameter to control none-ending (4d83418fa288)
* add method to create textcontentnavigator from path (ca81a8ae1fb6)
* make textnavigator creation prefix-able (0f9be2129c50)

### Fix

* parse collect content at end of loop (6c318e0092cb)
* do not shrink pages without header and footer (e106a93aa771)
* ensure that sort_byposition sorts correctly (5778c535c04c)
* fix PageTextContentNavigator to use header/footer to determine content (a3fabb733f2e)
* fix FixedFooterStrategy (0b4e6da6d654)
* do not use prefixed navigator data (69e5e57b57fc)
* fix inserting check of text bounds (96f35c24c87e)

### Documentation

* extend interface documentation (868f6746bc91)
* update doc string (36876ab907d3)
* add link to concrete class (266b481d8f21)
* add section for footer and header strategy (d7ea7a800965)
* format structure and link unit test to design decision (75bda061b073)
* improve navigation structure (8f6ec5f3c007)
* link strategy classes to documentation (75c3e778f59c)
* add basic groupme documentation structure (9ade279b8e13)

## v1.12.0

### Feature

* extend sentence parser (327ad5f068ad)
* analyse content till content ends (4a07467333da)
* add method to compare order of iamraw.Headline (361a2baeb459)
* add more complex multiline headline extractor (cadb567264c9)
* integrate multiline headline extractor (7303718265d4)
* normalize headlines to concentrate on content (7ed053708a1f)
* use font size strategy to determine headlines (c3b03e558a45)
* add first containerid to MultilineGroup (dace4b5f01e7)
* add prototype for MuliLine-Headline-Extractor (42709006dc2f)
* add method to determine sections from path (aa6873a9a04d)
* add method group multilines by line distance (ee7c899e92ef)
* add method to merge 2 groups (982901ce56a5)
* add method to group lines by gradient of line distance (ef11f9a2d144)
* add method to group text lines by font size (2e2b56a31b42)
* add method to create style without HighNotes (d6d7d88efd44)
* add method to copy TextStyle (009d0727bccc)
* extend sentence parser to parse content before loaded chapter (38b9f773b91e)
* merge sentences with headlines of to pages (7ae1190ba345)
* add methods to extract sentences and chapter content (0218406af1b5)
* reduce smallest headline size (49e32d20539a)
* add text feed to improve headline extractor strategy (3a1c0622733d)
* make sentence more robust against capitalisation (3b84685b9553)
* use new sentence splitter to split text (3ac0b96f5021)
* add method to remove high notes (82e5e8560434)
* add method to split text into sentences (b7730240651b)
* add footerlink to public interface (2f477c142aeb)
* add method to dump and load high notes (c3fa5f910bca)
* add footerlink extractor to parse text annotation from text (bdf2e38499a8)
* validate TextStyle after init to ensure correct definition (87f327b61016)
* use TextInfo information instead of FontStore definition (7f809ef33f7f)
* add method to extract HighNotes out of TextInfo (2f1469283dae)
* literature and footer reference (25ab355d8b6f)
* load required data for text processing from path (c05f2be52653)

### Fix

* fix chapter extractor (4b367d727081)
* merge sentences and headlines over pages correctly (a4c553c42599)
* fix parsing headlines before chapter starts (6480b95ad4c2)
* skip empty pages to avoid error in max calculation (26825879218c)
* correct import (3e19e804a8e7)
* fix return type of high notes extractor (9f28631fdd1c)
* extracting headlines on single page/few pages (bcc50dc497ba)
* fix unused imports (281037da4b1a)
* skip useless empty lines (1302e9cf346d)
* reduce layout offset to avoid missing last content line (3dec60786650)
* select correct page when creating PageTextNavigator selectively (8f540d6ddaf5)
* improve no-sentence message (2b37184fc62b)

### Documentation

* add design decision to introduce StrategyError (d6eb4f74d9c0)
* remove after moved to iamraw (7498c10a2cfa)
* extend interface documentation (c2b5388a31c6)
* extend interface documentation (9aea87dc9982)
* extend interface documentation (76580d18ec8c)
* use rst to document planned releases (28d1aefaa7eb)

## v1.11.0

### Feature

* support multiple sections on a single page (e18bf3a2810f)
* support multiple sections on page (12ea34e50687)
* use configo to handle holy values (97d13423bd65)
* add possible to shrink page left to right (0c8480feea82)
* add --pages information to toc feature (6028a5c05507)

### Fix

* use --all to make robust against interface changes (9bfe8f95d30d)
* correct loading order (0d30fb55a54a)
* enable undefined extraction (d8f099568691)
* fix empty style (9fcb7ed51ce3)
* activate test after improving font calculation (440efd1a43b0)
* use new font calculation (70e68c9d8d62)
* fix document with zero moving footer (811658ac1bac)

### Documentation

* fix output formatting (e6d61d9986cc)
* extend interface documentation (5be75966d391)
* extend interface documentation (9e5d466d601a)

## v1.10.0

### Feature

* skip empty pages with no ContentBorder (3fcdd09df807)
* extend headlines parser (e342d8a9c79c)
* improve footerheader judgement strategy (4a2e707cf64b)
* add title parser based on contemporary (0032c1a13991)
* limit max area of cluster to detecting equal numbers (ea18848fc4c8)
* expose max difference to improve testing/more variance (8af216486d97)
* extend footer page extraction area to match more examples (af4b3b11d00b)
* add first strategy to reduce miss extraction (d86da2a85955)
* add report to extraction strategy to determine quality of extraction (e107d6a630fc)
* refactor decider strategy (084027318c17)
* add method to create FooterHeaderDetectionStrategy from path (5894de58d20f)
* add method to create pagetextnavigator from path (946f95985ce9)
* replace with iamraw/serializeraw code (ad1bdaae212f)
* add --pages support (516c30b2b237)
* make section pages-able - move to serializeraw later (df7142749993)
* add --pages support to select pages to process (37f48c0455a9)

### Fix

* improve headline extractor (b4bddf40a0d1)
* fix docu to enable running Sphinx (f7f25cbad0a5)
* fix pagetextnavgiator creator (66de1e80fbca)

### Documentation

* fix spelling errors (812c3f4d2894)

## v1.9.0

### Feature

* extend potential footer area (3890b5ff98eb)
* extend footnotes regex to support more text data (8aa3028ae75d)
* extend footer load and dumper (fdd31976ae13)
* extend nolevel toc parser (af0180ad167f)
* support more than one header/footer area (74ad3f7b4238)
* use configo holy values and refactor FixedFooterStrategy (775a4c9ab8e5)
* use configo.holyvalue to describe holy values (725a4ebd3dc4)
* remove process-method, use result() directly (f10e4de25bd0)
* extend footer extract (c22c0bdf3ea9)
* add information of moving footer result (23e5dc746ecc)
* add footnotes extractor (09385eef21bf)
* add pagetextnavigator to Footer interface (b346a6c4998e)
* add page number strategy extractor (8457904e17ee)
* add pattern -number- as valid number pattern (151374f1fa0d)
* add options to control footer extraction (34bf991aaa44)
* enable one element cluster (10d437de9564)

### Fix

* make chapter assertion weaker, cause algorithm is really bad (61434c90fec9)
* fix fixed footer test (6498abd6c26e)
* extend possible header area to extend page number (a6a68fbac6df)
* only select result if one item matches (2232654451b8)

### Documentation

* fix spelling errors (0b49557ab28e)
* extend footer strategy documentation (e82aa0fe2b6c)
* document general and fixed footer strategy (6b4558154964)
* extend release plan (7a3ea0035f8e)
* move proposal and releases to better place (a660ad7de65e)
* reduce toc level to increase readability (3f6552dfccda)
* add first draft of release plan 1.10.0 (b454020a8b71)
* add file path of second example to moving header (631855001ba9)
* correct description of PageTextNavigator (dbff786bb629)
* add release plan for next release (b8ec820b3b94)

## v1.8.0

### Feature

* improve chapter extractor (86c175517928)
* reduce miss detection of toc lines (282ec3648d66)
* add method to count textual lines on page (33323c9a0665)
* add moving footer strategy (ed959d05aeee)
* add --test=generate to generate test resources only (ccb3d58c8638)
* add footer/header detection strategy management (b1a13e185f0c)
* add `DocumentObjectType` to determine object type on page position (dfc69228f4e7)
* expose result names of words processing to public API (b9868bd5e963)
* split strategy into 2 different approaches (10c66afa6fd5)
* extend headline parser (6e3b90c4fefa)
* add minimal required headlines to determine footer (e5688301bced)
* improve chapter detector (8993ba473018)
* improve robustness of toc regex parser (2e955765c017)

### Fix

* reduce log level of error in toc extractor (051bd9f03a50)
* handle non-level detection (da60c4367442)
* fix bounding box names (509c219cb5b2)
* ensure that text distance is positive (55506f7c9d0d)
* improve index detector (582e2d9f46c1)
* fix chapter extractor (0754c92919aa)

### Documentation

* add two proposal to describe gradient feature (92b889de0bba)
* add description to footer extraction strategies (8c85badd671c)

## v1.7.0

### Feature

* add method to parse to via regex (687eb753a78b)
* add method to create path to rawmaker-test-resources (61b727e0d554)

## v1.6.2

## v1.6.1

### Fix

* add workaround to support 'Diplomarbeit' till iamraw is patched (2c8b932fb6eb)

## v1.6.0

### Feature

* add order for more than one person without academic title (42a5a0f6dc79)
* extend person parser to support more pattern (754d21544515)
* extend person parser to support every Dipl.- title (b949859b5284)
* extend parser to parse Persons without academic title (53811cd64d93)

### Fix

* fix test resource to be in sync with pdf (3fbb4daab251)
* fix person parser without text before academic title (803ba580d840)
* ensure that order in document is preserved (6d8ace3d5e83)

### Documentation

* extend interface documentation of person parser (d898b8e59aff)

## v1.5.1

## v1.5.0

### Feature

* extend detector API with rawmaker configuration used in title extraction (f4052491791f)
* add general pattern to support Dr. med. bio. etc. (76814aee5b65)
* convert extracted TitlePage to yaml (df7fe27fd7d1)
* add work method of title parser (3446fcac1bbc)
* support date format "February 20, 2019" to use pydoc examples (d8416eae9d91)
* convert text to PageTextNavigator to use all parsing features (46da025adbc6)
* add title parser to complete parser (52684be9c585)
* activate multiprocessing and page selection (0d3ecbf59f52)
* add parser to parse title from hugest font (5af21ebf8abd)

### Fix

* handle no detected persons (38c361f9303b)
* increase the number of required digits for valid matrikel (4213b130cbba)
* add missing assertion after refactoring (5c021320f9a0)

## v1.4.0

### Feature

* add method to parse title text of title page (898365e6a8b1)
* add method to parse institute and courses of studies (248dfc715ea6)
* add method to parse the complete title page (1a5bbd2f8d4f)
* add method to split text in connected text blocks (53588f3373a9)
* add very simple parser to extract thesis type out of title page (885d6678b669)
* add method to parse matrikel number out of title page (6a3808c651c2)
* reduce required test power due reducing the count of pdfs under test (fa03e349d9de)
* add person parser to extract person with title from front-page (2f955a12f8d3)
* add parser to parse the date of title page (289ca8725aa7)
* add `detector` to analyze special features like title, toc etc. (7144438f6134)

### Fix

* fix massive interface changes after integration (e7a2917bc848)
* add missing test data generation (660377686f9d)

### Documentation

* add requirements for title parser (c4eb10ebef2a)

## v1.3.1

## v1.3.0

### Feature

* use real page size instead of constant box (981095e7e328)
* use `power` tool to generate test pdf data (cd1d689c8d14)

### Fix

* not every page contains a PageHeadlineList (b4a729861dca)
* workaround: skip broken boxed content (55d8f0939ae7)
* ignore single input file (19851678b09d)

## v1.2.10

### Feature

* extend debugging information of textprocessor (0a16551b2dde)

### Fix

* fix error in textprocessor to parse pyporting example (3eb9cc3e01db)

## v1.2.9

### Fix

* workaround: skip non content at the end (eecd435bce27)

## v1.2.8

### Fix

* add workaround to fix problem with chapter partition (7b095fdb8622)

## v1.2.7

### Feature

* extend logging to ease debugging (1276054bfae0)

### Fix

* fix headline regex to avoid enormous/infinite runtime (5d51f1c252f6)

## v1.2.6

### Feature

* add error message to assertion (177549e1a139)

## v1.2.5

## v1.2.4

## v1.2.3

## v1.2.2

### Fix

* fix output name of toc generation (a3371f9e4dae)

## v1.2.1

## v1.2.0

### Feature

* add `words` feature to word command line tool (2b03518dbea1)
* connect text with collected lists and boxed features (ba5bfc2cd471)
* connect objects with undefined index (20d71eaa36c9)
*  extend merge_content with optional undefined index's `uindex` (a580a94a1031)
* convert lists to str (7950e900ae61)
* add ids of merged paragraphs (412af42fe44a)
* improve textnavigator (12e13d62f3a6)
* add lru cache to improve speed (1357cf7cf7f8)
* use @checkdatatype feature to ensure data input (d883d9bf2f8b)
* add boxed-feature to `words` executable (7405a621ef91)
* add method to lookup boxid to `BoundingBox` (a695103afd98)
* add feature to extract boxes from document (3535f1d95201)
* add hint of page for skipped item (eaf2944fcbcf)
* add list to workplan/command line interface (1b09ddeb8a7f)

### Fix

* print skipped content on info level only (6031f5cd9c5e)
* decrease level of logging to reduce verbosity of logging (87aeeecc4909)
* skip non parsed area (7cc2933163f0)
* set default value for non existing header or footer (9c56180f983d)
* remove index output check - not every document contains a document (4f23ceac766b)
* enable using raw inputs instead of objects (36c562dda2a5)

### Documentation

* extend interface documentation (5d59f5983ec5)
* replace print with p to avoid collecting when searching `print` (1f375b2641b1)

## v1.1.0

### Feature

* ensure that passed border and horizontals are resources (8175a0eebf26)
* use contentborder to determine the correct undefined index (2dd24d487f0e)
* add method to dump and load extract list result (93801ffa7e1c)
* add method to extract lists (f2f43071df14)
* add text feed text detection `merge_content` (9d59df827a83)
* extend list extractor (95c597269675)
* add possible space to detection pattern (cef71ddda0a6)
* extend parser with plus, minus and dotted parser (1e52bea95218)
* add undefined to content converter (52f210c3de38)
* reduce confusion when initializing PageTextContentNavigator (af2c2a27d877)
* add ? to mark that result is not clear (84136bc7d83d)
* add parsing non headline page and reorder class (b73741344e65)
* set default container to None to fail faster (2a8efa8763d8)
* add collect on pages without any headline but text content (21b985d7e514)
* add text and text- and headlines-extractor to working plan (aa8dbcd5528d)
* add method to extract text and detect non text areas (76fdf318d7f1)
* fontstore - provide offset as class property (b3da3cabf3d3)
* add method to join multiple list to one list (b07ebfee36e2)
* add method to determine fontid of Font (ea478b459b27)
* add field page to headline (85ac9a39ce1c)
* remove None elements from white pages output (5ef13af1d62c)
* add work method to use headlines in command line tool (4855c5516818)
* don't write entree for empty page/input (b662c4871a0b)
* expand method to dump and load sections (55378678e006)
* add method to dump and load headlines (dd14a30dc538)
* save containerid for grouping text areas (d649ce931448)

### Fix

* fix list pattern detector (03944c60798f)
* fix offset bug (35b70d7f4fd3)
* fix multiple parser (80408b299fe9)
* rename field to chapter (af49c6abdc63)
* fix passing empty elements to max size detection (211c75f7fbcb)
* fix chapter index offset (e50b5f842ba0)
* fix extracting all chapter (e3dfd023299a)

## v1.0.0

### Feature

* use central constant to describe START and END of a page (e483da22dc64)

### Fix

* use new BoundingBox-API (b7030ad511c7)
* flip y-coordinate and use new BoundingBox-API (b345b3187d6d)

### Documentation

* extend interface documentation (1653b4ab9b37)

## v0.4.2

### Feature

* add method to determine font distances based on TextBounds (4f3112995622)
* determine font level based on font-size/position information (d9873544e303)
* use central roundme method to avoid code duplicates (0f7b89513623)
* ensure rawmaker version for generating test data (e193c6257036)
* add FontContentStore to analyze fonts on current content page (a36442601646)
* add method to determine fonts from text sequence (39a7ef42b7ad)
* add headline extractor - not finished yet (49be003da2aa)
* add textnavigator which ignores footer and header information (b82c5072f299)
* add method to extract footer area from page (cc6b51479033)
* add method to determine font size of normal text of document (6d822e7159cb)
* add templates for new features style, text, words (f64c5e82362d)
* add title to chapter (d16b6883c906)
* add method to extract chapter out of `Sections` (03e581891ab5)
* extend interface documentation add some assertion (d55ffbe6ca1d)
* group sections to determine document structure (b6978f174be6)
* count ". ." instead of "." (74d35becd031)
* add extraction of chapter with incomplete chapter title (12c1ed5b533e)
* add separate serializing of title and level (7bff73817054)
* add `dump_chapter` method (f692e91bd8e3)

### Fix

* fix offset index (9b89acc24639)
* fix textprocessor accessing the right token (4704f3d4ee21)
* fix font store access via fontid (9ef271d37c7b)
* fix imports to new serializeraw version (f6245ad8c480)
* fix missing refactored package (89a1cccdaa0d)
* fix __len__ method of sections (83bcd87a1db0)
* remove percentage of page number, take only full page numbers (2a8367f49fe6)
* fix to new feature interface (44ff6236456f)

### Documentation

* extend interface documentation of FontStore (1bfa5c246f53)
* extend toc interface documentation (3f13246aa9eb)
* add hint to investigate to pipeline (b2b7805b84c6)

## v0.4.1

### Feature

* extend list parser with +, -, dotted (16d29b753659)
* add feature to extract list out of documents (b491dedc4c8f)
* add method to determine font feed and font distance (6cd43c39f390)
* add text font extractor (0bb6eb60e8e1)
* extract BoundingBoxes out of PageTextNavigator (256c928b39d9)
* start new feature words as text processor (e949eff36466)

### Documentation

* add required resource in words description (d58d88ad4f24)
* add description with `words` functionality (4ec3cc3a14f6)

## v0.4.0

### Feature

* add tableofcontent and remove unused page number (c04d33eab6ec)
* extend workplan to run section feature (fe5295dc4c9b)
* add sections to combine title, index, chapter, toc (8b8a77ae320d)
* add chapter feature to determine start of chapter (7813e1acd82b)
* add recursive feature - experimental, move to utila (ce1932e9840e)
* add white page feature detector (f10d88713fcb)
* compute percent to page size and backwards (670a6053a8b9)
* add method to determine content in the middle of a page (c195c572192d)
* add footer and header extractor (99273d9bbd61)
* create work method for toc feature (bb9d5347f7f4)
* create workplan with toc, index and title (dd7424e93b78)
* add result dump to work method of title (e2a2f25f376a)
* dump result of `index` feature (53128d220e84)
* add methods to load and dump list of likelihoods (7329bf12edd3)
* add title extractor to determine the likelihood of title-page (bee7524d03c2)
* add toc extractor to compute likelihood of table of content (bc49865b3c19)
* add index locator to identify the likelihood of index-page (dc2e52950f97)
* add basic implementation of sections data structure (d1978c06e548)
* add new cmdline tool `sections` to analyse pdf structure (27302a06976c)
* remove featurepath to reduce code duplication (4e1d2fc71ce6)

### Fix

* save class name as single string (cfda1e11e54e)
* add removed chapter number again (6b1cde6b3e7f)
* add text as standard page (23b174891369)
* add missing test resources (00a5edc7a105)
* dump white page result as str (22740013416f)
* do not change the order of content (42a6aad61160)
* problems with page numbers are fixed, this is not necessary (95ed1ee33774)
* increase range of right result cause of round single entrees of list (c20c6c4dd145)
* increase malus per page, to improve title locator performance (8535305b5e73)
* fix project configuration with correct project name (88d932d6de5a)
* make groupme version equal to current hey version (94607f95bdef)

### Documentation

* update summarisation of hey (af69c36d3ca6)
* extend interface documentation (328ad364cbeb)
* extend interface document of `index` feature (acab70e7f7c9)
* extend restructured documentation (84775dbb751a)

## v0.3.0

### Feature

* extend approach to determine table of content (6e2640173603)
* sort pagenumber output by pdf-page (f2a4484e809b)
* use new feature interface for chpater, footer, toc (5446c45c74ab)
* introduce new feature pattern form utila (f3ef71e390ac)
* structure is no longer a feature, it is more supporting code (4f92c27a73a4)
* save bounding of page number (87c75e716e49)
* add method to determine page number (6a3bf2a8cc13)
* add 2 algorithms to cluster text per page and position (0bb887d31fcb)
* add method to load textpagenavigator from text/position source (c5a4b5059eee)
* add textnavigator to simple iterate depending on position (4c3d67b57077)

### Fix

* return None when no section is located on page (9d3954075479)
* allow `:` in headlines (a7225fdebdcd)
* remove final newline of textcontainer (45971fbc7c74)

### Documentation

* extend readme with basic information (b9e372cd9926)

## v0.2.6

### Fix

* use new test API (d635ea101628)

## v0.2.5

## v0.2.4

## v0.2.3

## v0.2.2

### Feature

* change command line interface to folder architecture (16bd2ac41f4b)

### Fix

* remove compression, we will use folders (627a4412b6db)

## v0.2.1

## v0.2.0

### Feature

* add chapter extractor to cmdline (a4764811ff4b)

### Fix

* remove package before test installation (97ad07d229dc)
* add missing package include (401d3d685443)

## v0.1.0

### Feature

* move groupme to hey mono repo (b643494192aa)

## v0.0.0 Initial release
