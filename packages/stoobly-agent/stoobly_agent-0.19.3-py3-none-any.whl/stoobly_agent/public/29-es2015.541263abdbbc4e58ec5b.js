(window.webpackJsonp=window.webpackJsonp||[]).push([[29],{"6qw8":function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M20 6H4l8 4.99zM4 8v10h16V8l-8 5z" fill="currentColor"/><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 2l-8 4.99L4 6h16zm0 12H4V8l8 5l8-5v10z" fill="currentColor"/>',width:24,height:24}},DkW8:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M19 3H5v12.93l7 4.66l7-4.67V3zm-9 13l-4-4l1.41-1.41l2.58 2.58l6.59-6.59L18 8l-8 8z" fill="currentColor"/><path d="M19 1H5c-1.1 0-1.99.9-1.99 2L3 15.93c0 .69.35 1.3.88 1.66L12 23l8.11-5.41c.53-.36.88-.97.88-1.66L21 3c0-1.1-.9-2-2-2zm-7 19.6l-7-4.66V3h14v12.93l-7 4.67zm-2.01-7.42l-2.58-2.59L6 12l4 4l8-8l-1.42-1.42z" fill="currentColor"/>',width:24,height:24}},PGLt:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M15 17H9v-1H5v3h14v-3h-4zM4 14h5v-3h6v3h5V9H4z" fill="currentColor"/><path d="M20 7h-4V5l-2-2h-4L8 5v2H4c-1.1 0-2 .9-2 2v5c0 .75.4 1.38 1 1.73V19c0 1.11.89 2 2 2h14c1.11 0 2-.89 2-2v-3.28c.59-.35 1-.99 1-1.72V9c0-1.1-.9-2-2-2zM10 5h4v2h-4V5zm9 14H5v-3h4v1h6v-1h4v3zm-8-4v-2h2v2h-2zm9-1h-5v-3H9v3H4V9h16v5z" fill="currentColor"/>',width:24,height:24}},QKIt:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M19.47 9.16a8.027 8.027 0 0 0-7.01-5.14l2 4.71l5.01.43zm-7.93-5.14c-3.22.18-5.92 2.27-7.02 5.15l5.02-.43l2-4.72zm-7.31 6.12C4.08 10.74 4 11.36 4 12c0 2.48 1.14 4.7 2.91 6.17l1.11-4.75l-3.79-3.28zm15.54-.01l-3.79 3.28l1.1 4.76A7.99 7.99 0 0 0 20 12c0-.64-.09-1.27-.23-1.87zM7.84 18.82c1.21.74 2.63 1.18 4.15 1.18c1.53 0 2.95-.44 4.17-1.18L12 16.31l-4.16 2.51z" fill="currentColor"/><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm7.48 7.16l-5.01-.43l-2-4.71c3.21.19 5.91 2.27 7.01 5.14zM12 8.06l1.09 2.56l2.78.24l-2.11 1.83l.63 2.73L12 13.98l-2.39 1.44l.63-2.72l-2.11-1.83l2.78-.24L12 8.06zm-.46-4.04l-2 4.72l-5.02.43c1.1-2.88 3.8-4.97 7.02-5.15zM4 12c0-.64.08-1.26.23-1.86l3.79 3.28l-1.11 4.75A8.014 8.014 0 0 1 4 12zm7.99 8c-1.52 0-2.94-.44-4.15-1.18L12 16.31l4.16 2.51A8.008 8.008 0 0 1 11.99 20zm5.1-1.83l-1.1-4.76l3.79-3.28c.13.6.22 1.23.22 1.87c0 2.48-1.14 4.7-2.91 6.17z" fill="currentColor"/>',width:24,height:24}},XFqH:function(l,n,u){"use strict";u.r(n),u.d(n,"PricingModuleNgFactory",function(){return K});var t=u("8Y7J");class i{}var e=u("pMnS"),c=u("VDRc"),a=u("/q54"),o=u("l+Q0"),s=u("cUpR"),r=u("SVse"),b=u("ura0"),d=u("1Xc+"),p=u("Dxy4"),h=u("YEUz"),m=u("omvX"),f=u("A4cF"),x=u("9gLZ"),g=u("iInd"),y=u("DkW8"),v=u.n(y),z=u("PGLt"),M=u.n(z),L=u("6qw8"),A=u.n(L),C=u("reS8"),w=u.n(C),k=u("QKIt"),E=u.n(k),_=u("XXSj");class S{constructor(l,n,u,t,i){this.layoutConfigService=l,this.route=n,this.router=u,this.userResource=t,this.userDataService=i,this.icBeenhere=v.a,this.icStars=E.a,this.icBusinessCenter=M.a,this.icPhoneInTalk=w.a,this.icMail=A.a,this.theme=_.a,this.layoutConfigService.setIkaros()}ngOnInit(){this.plans=this.route.snapshot.data.plans,this.subscription=this.route.snapshot.data.subscription}buy(l){const n=this.route.snapshot;n.queryParams.organization_id?this.showBuy(l,n.queryParams.organization_id):this.userDataService.user?this.userResource.profile({organization:!0}).subscribe(n=>{const{organization_id:u}=n;this.showBuy(l,u)}):this.router.navigate(["/login"])}showBuy(l,n){this.router.navigate(["/subscriptions/buy"],{queryParams:{organization_id:n,plan_id:l.id}})}isSubscribed(l){return!!this.subscription&&l.id==this.subscription.plan.id}ngOnDestroy(){this.layoutConfigService.setZeus()}}var O=u("U9Lm"),Y=u("9IlP"),I=u("m/Wb"),H=t.yb({encapsulation:0,styles:[[".header[_ngcontent-%COMP%]{background-color:var(--background-base);background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%23e6e6e6' stroke-width='1'%3E%3Cpath d='M769 229L1037 260.9M927 880L731 737 520 660 309 538 40 599 295 764 126.5 879.5 40 599-197 493 102 382-31 229 126.5 79.5-69-63'/%3E%3Cpath d='M-31 229L237 261 390 382 603 493 308.5 537.5 101.5 381.5M370 905L295 764'/%3E%3Cpath d='M520 660L578 842 731 737 840 599 603 493 520 660 295 764 309 538 390 382 539 269 769 229 577.5 41.5 370 105 295 -36 126.5 79.5 237 261 102 382 40 599 -69 737 127 880'/%3E%3Cpath d='M520-140L578.5 42.5 731-63M603 493L539 269 237 261 370 105M902 382L539 269M390 382L102 382'/%3E%3Cpath d='M-222 42L126.5 79.5 370 105 539 269 577.5 41.5 927 80 769 229 902 382 603 493 731 737M295-36L577.5 41.5M578 842L295 764M40-201L127 80M102 382L-261 269'/%3E%3C/g%3E%3Cg fill='%23e6e6e6'%3E%3Ccircle cx='769' cy='229' r='5'/%3E%3Ccircle cx='539' cy='269' r='5'/%3E%3Ccircle cx='603' cy='493' r='5'/%3E%3Ccircle cx='731' cy='737' r='5'/%3E%3Ccircle cx='520' cy='660' r='5'/%3E%3Ccircle cx='309' cy='538' r='5'/%3E%3Ccircle cx='295' cy='764' r='5'/%3E%3Ccircle cx='40' cy='599' r='5'/%3E%3Ccircle cx='102' cy='382' r='5'/%3E%3Ccircle cx='127' cy='80' r='5'/%3E%3Ccircle cx='370' cy='105' r='5'/%3E%3Ccircle cx='578' cy='42' r='5'/%3E%3Ccircle cx='237' cy='261' r='5'/%3E%3Ccircle cx='390' cy='382' r='5'/%3E%3C/g%3E%3C/svg%3E\")}.footer[_ngcontent-%COMP%]{background-image:url(/assets/img/illustrations/it_support.svg);background-position:100% 100%;background-repeat:no-repeat;background-size:250px;padding-bottom:250px}@media (min-width:960px){.footer[_ngcontent-%COMP%]{padding-bottom:1rem}}.text-white[_ngcontent-%COMP%]{color:#fff!important}"]],data:{animation:[{type:7,name:"stagger",definitions:[{type:1,expr:"* => *",animation:[{type:11,selector:"@fadeInUp, @fadeInRight, @scaleIn",animation:{type:12,timings:60,animation:{type:9,options:null}},options:{optional:!0}}],options:null}],options:{}},{type:7,name:"fadeInUp",definitions:[{type:1,expr:":enter",animation:[{type:6,styles:{transform:"translateY(20px)",opacity:0},offset:null},{type:4,styles:{type:6,styles:{transform:"translateY(0)",opacity:1},offset:null},timings:"400ms cubic-bezier(0.35, 0, 0.25, 1)"}],options:null}],options:{}}]}});function j(l){return t.bc(0,[(l()(),t.Ab(0,0,null,null,1,"span",[],null,null,null,null,null)),(l()(),t.Yb(1,null,[" "," "]))],null,function(l,n){l(n,1,0,0===n.parent.context.$implicit.charge_amount?"CONTINUE FREE":n.parent.context.$implicit.charge_amount?"GET STARTED":"CONTACT SALES")})}function P(l){return t.bc(0,[(l()(),t.Ab(0,0,null,null,1,"span",[],null,null,null,null,null)),(l()(),t.Yb(-1,null,[" SUBSCRIBED "]))],null,null)}function U(l){return t.bc(0,[(l()(),t.Ab(0,0,null,null,48,"div",[["class","card p-6"],["fxFlex",""],["fxLayout","column"],["fxLayoutAlign","start center"]],[[24,"@fadeInUp",0]],null,null,null,null)),t.zb(1,671744,null,0,c.d,[t.l,a.i,c.k,a.f],{fxLayout:[0,"fxLayout"]},null),t.zb(2,671744,null,0,c.c,[t.l,a.i,c.i,a.f],{fxLayoutAlign:[0,"fxLayoutAlign"]},null),t.zb(3,737280,null,0,c.b,[t.l,a.i,a.e,c.h,a.f],{fxFlex:[0,"fxFlex"]},null),(l()(),t.Ab(4,0,null,null,5,"div",[["class","inline-block p-6 rounded-full text-primary-500 mx-auto"],["fxLayout","row"],["fxLayoutAlign","center center"]],[[4,"background-color",null]],null,null,null,null)),t.zb(5,671744,null,0,c.d,[t.l,a.i,c.k,a.f],{fxLayout:[0,"fxLayout"]},null),t.zb(6,671744,null,0,c.c,[t.l,a.i,c.i,a.f],{fxLayoutAlign:[0,"fxLayoutAlign"]},null),t.Sb(7,2),(l()(),t.Ab(8,0,null,null,1,"ic-icon",[["size","48px"]],[[2,"ic-inline",null],[4,"font-size",null],[8,"innerHTML",1]],null,null,null,null)),t.zb(9,606208,null,0,o.a,[s.b],{icon:[0,"icon"],size:[1,"size"]},null),(l()(),t.Ab(10,0,null,null,1,"h2",[["class","headline mt-5"]],null,null,null,null,null)),(l()(),t.Yb(11,null,["",""])),(l()(),t.Ab(12,0,null,null,1,"h4",[["class","mb-5 text-center text-secondary"]],null,null,null,null,null)),(l()(),t.Yb(13,null,["",""])),(l()(),t.Ab(14,0,null,null,3,"div",[["class","body-1"]],null,null,null,null,null)),(l()(),t.Ab(15,0,null,null,1,"span",[["class","body-2"]],null,null,null,null,null)),(l()(),t.Yb(16,null,["",""])),(l()(),t.Yb(-1,null,[" Users"])),(l()(),t.Ab(18,0,null,null,3,"div",[["class","body-1"]],null,null,null,null,null)),(l()(),t.Ab(19,0,null,null,1,"span",[["class","body-2"]],null,null,null,null,null)),(l()(),t.Yb(20,null,["",""])),(l()(),t.Yb(-1,null,[" Projects"])),(l()(),t.Ab(22,0,null,null,3,"div",[["class","body-1"]],null,null,null,null,null)),(l()(),t.Ab(23,0,null,null,1,"span",[["class","body-2"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["10GB"])),(l()(),t.Yb(-1,null,[" Storage"])),(l()(),t.Ab(26,0,null,null,3,"div",[["class","body-1"]],null,null,null,null,null)),(l()(),t.Ab(27,0,null,null,1,"span",[["class","body-2"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["Basic"])),(l()(),t.Yb(-1,null,[" Support"])),(l()(),t.Ab(30,0,null,null,12,"div",[],null,null,null,null,null)),t.zb(31,278528,null,0,r.j,[t.u,t.v,t.l,t.G],{ngClass:[0,"ngClass"]},null),t.Rb(32,{"text-white":0}),t.zb(33,933888,null,0,b.a,[t.l,a.i,a.f,t.u,t.v,t.G,[6,r.j]],{ngClass:[0,"ngClass"]},null),t.Rb(34,{"text-white":0}),(l()(),t.Ab(35,0,null,null,5,"h3",[["class","display-2 font-bold mt-6"]],null,null,null,null,null)),(l()(),t.Yb(36,null,[" ",""])),(l()(),t.Ab(37,0,null,null,3,"span",[["class","headline align-top"],["ngClass","{'text-secondary': plan.charge_amount}"]],null,null,null,null,null)),t.zb(38,278528,null,0,r.j,[t.u,t.v,t.l,t.G],{klass:[0,"klass"],ngClass:[1,"ngClass"]},null),t.zb(39,933888,null,0,b.a,[t.l,a.i,a.f,t.u,t.v,t.G,[6,r.j]],{ngClass:[0,"ngClass"],klass:[1,"klass"]},null),(l()(),t.Yb(-1,null,["$"])),(l()(),t.Ab(41,0,null,null,1,"span",[],null,null,null,null,null)),(l()(),t.Yb(-1,null,["per user/month"])),(l()(),t.Ab(43,0,null,null,5,"button",[["class","mt-5 max-w-full w-200 mat-focus-indicator"],["color","primary"],["mat-raised-button",""],["type","button"]],[[1,"disabled",0],[2,"_mat-animation-noopable",null],[2,"mat-button-disabled",null]],[[null,"click"]],function(l,n,u){var t=!0;return"click"===n&&(t=!1!==l.component.buy(l.context.$implicit)&&t),t},d.d,d.b)),t.zb(44,4374528,null,0,p.b,[t.l,h.h,[2,m.a]],{disabled:[0,"disabled"],color:[1,"color"]},null),(l()(),t.jb(16777216,null,0,1,null,j)),t.zb(46,16384,null,0,r.m,[t.R,t.O],{ngIf:[0,"ngIf"]},null),(l()(),t.jb(16777216,null,0,1,null,P)),t.zb(48,16384,null,0,r.m,[t.R,t.O],{ngIf:[0,"ngIf"]},null)],function(l,n){var u=n.component;l(n,1,0,"column"),l(n,2,0,"start center"),l(n,3,0,""),l(n,5,0,"row"),l(n,6,0,"center center"),l(n,9,0,u.icBeenhere,"48px");var t=l(n,32,0,null===n.context.$implicit.charge_amount);l(n,31,0,t);var i=l(n,34,0,null===n.context.$implicit.charge_amount);l(n,33,0,i),l(n,38,0,"headline align-top","{'text-secondary': plan.charge_amount}"),l(n,39,0,"{'text-secondary': plan.charge_amount}","headline align-top"),l(n,44,0,u.isSubscribed(n.context.$implicit),"primary"),l(n,46,0,!u.isSubscribed(n.context.$implicit)),l(n,48,0,u.isSubscribed(n.context.$implicit))},function(l,n){var u=n.component;l(n,0,0,void 0);var i=t.Zb(n,4,0,l(n,7,0,t.Ob(n.parent,0),u.theme.colors.primary[500],.9));l(n,4,0,i),l(n,8,0,t.Ob(n,9).inline,t.Ob(n,9).size,t.Ob(n,9).iconHTML),l(n,11,0,n.context.$implicit.name),l(n,13,0,n.context.$implicit.description),l(n,16,0,n.context.$implicit.max_seats),l(n,20,0,n.context.$implicit.max_projects),l(n,36,0,n.context.$implicit.charge_amount),l(n,43,0,t.Ob(n,44).disabled||null,"NoopAnimations"===t.Ob(n,44)._animationMode,t.Ob(n,44).disabled)})}function T(l){return t.bc(0,[t.Qb(0,f.a,[]),(l()(),t.Ab(1,0,null,null,37,"div",[],[[24,"@stagger",0]],null,null,null,null)),(l()(),t.Ab(2,0,null,null,4,"div",[["class","bg-card py-16 px-gutter"]],null,null,null,null,null)),(l()(),t.Ab(3,0,null,null,1,"h1",[["class","display-2 mt-0 mb-4 text-center"]],[[24,"@fadeInUp",0]],null,null,null,null)),(l()(),t.Yb(-1,null,["Pricing & Plans"])),(l()(),t.Ab(5,0,null,null,1,"h2",[["class","subheading-2 text-hint text-center max-w-lg mx-auto m-0"]],[[24,"@fadeInUp",0]],null,null,null,null)),(l()(),t.Yb(-1,null,["Simple, transparent pricing."])),(l()(),t.Ab(7,0,null,null,5,"div",[["class","my-12 container"],["fxLayout","row"],["fxLayout.xs","column"],["fxLayoutAlign","start start"],["fxLayoutAlign.xs","start stretch"],["fxLayoutGap","24px"]],null,null,null,null,null)),t.zb(8,671744,null,0,c.d,[t.l,a.i,c.k,a.f],{fxLayout:[0,"fxLayout"],"fxLayout.xs":[1,"fxLayout.xs"]},null),t.zb(9,1720320,null,0,c.e,[t.l,t.B,x.b,a.i,c.j,a.f],{fxLayoutGap:[0,"fxLayoutGap"]},null),t.zb(10,671744,null,0,c.c,[t.l,a.i,c.i,a.f],{fxLayoutAlign:[0,"fxLayoutAlign"],"fxLayoutAlign.xs":[1,"fxLayoutAlign.xs"]},null),(l()(),t.jb(16777216,null,null,1,null,U)),t.zb(12,278528,null,0,r.l,[t.R,t.O,t.u],{ngForOf:[0,"ngForOf"]},null),(l()(),t.Ab(13,0,null,null,25,"div",[["class","bg-card py-16 px-gutter footer"]],[[24,"@fadeInUp",0]],null,null,null,null)),(l()(),t.Ab(14,0,null,null,1,"h2",[["class","display-1 mt-0 mb-4 text-center"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["Still have questions?"])),(l()(),t.Ab(16,0,null,null,1,"h3",[["class","subheading-2 text-hint text-center max-w-lg mx-auto m-0"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart."])),(l()(),t.Ab(18,0,null,null,20,"div",[["class","mt-16 max-w-3xl mx-auto flex flex-col md:flex-row"]],null,null,null,null,null)),(l()(),t.Ab(19,0,null,null,9,"a",[["class","text-center p-6 border rounded md:w-1/2 md:mx-2"],["routerLinkActive",""]],null,null,null,null,null)),t.zb(20,1720320,null,2,g.r,[g.p,t.l,t.G,t.h,[2,g.q],[2,g.s]],{routerLinkActive:[0,"routerLinkActive"]},null),t.Ub(603979776,1,{links:1}),t.Ub(603979776,2,{linksWithHrefs:1}),(l()(),t.Ab(23,0,null,null,1,"ic-icon",[["class","text-hint"],["size","42px"]],[[2,"ic-inline",null],[4,"font-size",null],[8,"innerHTML",1]],null,null,null,null)),t.zb(24,606208,null,0,o.a,[s.b],{icon:[0,"icon"],size:[1,"size"]},null),(l()(),t.Ab(25,0,null,null,1,"h3",[["class","title mb-0 mt-4"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["+1 (840) 423-3404"])),(l()(),t.Ab(27,0,null,null,1,"h4",[["class","subheading-2 m-0 text-hint"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["Call us anytime for a quick solution"])),(l()(),t.Ab(29,0,null,null,9,"a",[["class","text-center p-6 border rounded md:w-1/2 md:mx-2"],["routerLinkActive",""]],null,null,null,null,null)),t.zb(30,1720320,null,2,g.r,[g.p,t.l,t.G,t.h,[2,g.q],[2,g.s]],{routerLinkActive:[0,"routerLinkActive"]},null),t.Ub(603979776,3,{links:1}),t.Ub(603979776,4,{linksWithHrefs:1}),(l()(),t.Ab(33,0,null,null,1,"ic-icon",[["class","text-hint"],["size","42px"]],[[2,"ic-inline",null],[4,"font-size",null],[8,"innerHTML",1]],null,null,null,null)),t.zb(34,606208,null,0,o.a,[s.b],{icon:[0,"icon"],size:[1,"size"]},null),(l()(),t.Ab(35,0,null,null,1,"h3",[["class","title mb-0 mt-4"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["support@example.com"])),(l()(),t.Ab(37,0,null,null,1,"h4",[["class","subheading-2 m-0 text-hint"]],null,null,null,null,null)),(l()(),t.Yb(-1,null,["Send us a mail to resolve your issue"]))],function(l,n){var u=n.component;l(n,8,0,"row","column"),l(n,9,0,"24px"),l(n,10,0,"start start","start stretch"),l(n,12,0,u.plans),l(n,20,0,""),l(n,24,0,u.icPhoneInTalk,"42px"),l(n,30,0,""),l(n,34,0,u.icMail,"42px")},function(l,n){l(n,1,0,void 0),l(n,3,0,void 0),l(n,5,0,void 0),l(n,13,0,void 0),l(n,23,0,t.Ob(n,24).inline,t.Ob(n,24).size,t.Ob(n,24).iconHTML),l(n,33,0,t.Ob(n,34).inline,t.Ob(n,34).size,t.Ob(n,34).iconHTML)})}function $(l){return t.bc(0,[(l()(),t.Ab(0,0,null,null,1,"pricing",[],null,null,null,T,H)),t.zb(1,245760,null,0,S,[O.a,g.a,g.p,Y.a,I.a],null,null)],function(l,n){l(n,1,0)},null)}var B=t.wb("pricing",S,$,{},{},[]),G=u("1O3W"),R=u("rJgo");class V{}var q=u("Nhcz"),D=u("u9T3"),F=u("UhP/"),N=u("SCoL"),W=u("1z/I"),X=u("7KAL"),J=u("Tj54"),Q=u("Chvm"),K=t.xb(i,[],function(l){return t.Lb([t.Mb(512,t.j,t.bb,[[8,[e.a,B]],[3,t.j],t.z]),t.Mb(4608,r.o,r.n,[t.w]),t.Mb(5120,t.b,function(l,n){return[a.j(l,n)]},[r.d,t.D]),t.Mb(4608,G.c,G.c,[G.j,G.e,t.j,G.i,G.f,t.t,t.B,r.d,x.b,r.h,G.h]),t.Mb(5120,G.k,G.l,[G.c]),t.Mb(5120,R.d,R.k,[G.c]),t.Mb(1073742336,r.c,r.c,[]),t.Mb(1073742336,g.t,g.t,[[2,g.z],[2,g.p]]),t.Mb(1073742336,V,V,[]),t.Mb(1073742336,o.b,o.b,[]),t.Mb(1073742336,a.c,a.c,[]),t.Mb(1073742336,x.a,x.a,[]),t.Mb(1073742336,c.g,c.g,[]),t.Mb(1073742336,b.c,b.c,[]),t.Mb(1073742336,q.a,q.a,[]),t.Mb(1073742336,D.a,D.a,[a.g,t.D]),t.Mb(1073742336,F.l,F.l,[h.j,[2,F.e],r.d]),t.Mb(1073742336,N.b,N.b,[]),t.Mb(1073742336,F.w,F.w,[]),t.Mb(1073742336,p.c,p.c,[]),t.Mb(1073742336,W.g,W.g,[]),t.Mb(1073742336,X.b,X.b,[]),t.Mb(1073742336,X.d,X.d,[]),t.Mb(1073742336,G.g,G.g,[]),t.Mb(1073742336,R.j,R.j,[]),t.Mb(1073742336,R.h,R.h,[]),t.Mb(1073742336,J.c,J.c,[]),t.Mb(1073742336,Q.a,Q.a,[]),t.Mb(1073742336,i,i,[]),t.Mb(1024,g.n,function(){return[[{path:"",component:S}]]},[])])})},reS8:function(l,n){n.__esModule=!0,n.default={body:'<path opacity=".3" d="M6.54 5h-1.5c.09 1.32.34 2.58.75 3.79l1.2-1.21c-.24-.83-.39-1.7-.45-2.58zm8.66 13.21c1.21.41 2.48.67 3.8.76v-1.5c-.88-.07-1.75-.22-2.6-.45l-1.2 1.19z" fill="currentColor"/><path d="M15 12h2c0-2.76-2.24-5-5-5v2c1.66 0 3 1.34 3 3zm4 0h2a9 9 0 0 0-9-9v2c3.87 0 7 3.13 7 7zm1 3.5c-1.25 0-2.45-.2-3.57-.57c-.1-.03-.21-.05-.31-.05c-.26 0-.51.1-.71.29l-2.2 2.2a15.045 15.045 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1c0 9.39 7.61 17 17 17c.55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1zM5.03 5h1.5c.07.88.22 1.75.45 2.58l-1.2 1.21c-.4-1.21-.66-2.47-.75-3.79zM19 18.97c-1.32-.09-2.6-.35-3.8-.76l1.2-1.2c.85.24 1.72.39 2.6.45v1.51z" fill="currentColor"/>',width:24,height:24}}}]);